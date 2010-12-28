%global major_minor 3.1

Name:             glusterfs
Version:          %{major_minor}.1
Release:          1%{?dist}
Summary:          Clustered file-system

Group:            System Environment/Base
License:          AGPLv3
URL:              http://www.gluster.org/
Source0:          http://download.gluster.com/pub/gluster/glusterfs/%{major_minor}/%{version}/glusterfs-%{version}.tar.gz
Source1:          glusterd.init
Source2:          glusterd.sysconfig
Source3:          umount.glusterfs
Source4:          glusterfs-fuse.logrotate
Source5:          glusterd.logrotate
# Legacy server
Source11:         glusterfsd.init
Source12:         glusterfsd.sysconfig
Source15: 	      glusterfsd.logrotate

BuildRequires:    bison
BuildRequires:    flex
BuildRequires:    gcc
BuildRequires:    make

Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/service
Requires(preun):  /sbin/chkconfig
Requires(postun): /sbin/service

Obsoletes:        %{name}-libs <= 2.0.0
Obsoletes:        %{name}-common < 3.1.0
Provides:         %{name}-libs = %{version}-%{release}
Provides:         %{name}-common = %{version}-%{release}

%description
GlusterFS is a clustered file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package includes the glusterfs binary, the glusterfsd daemon and the
gluster command line, libglusterfs and glusterfs translator modules common to
both GlusterFS server and client framework.

%package rdma
Summary:          Support for ib-verbs
Group:            Applications/File
Requires:         %{name} = %{version}-%{release}
BuildRequires:    libibverbs-devel

%description rdma
GlusterFS is a clustered file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides support to ib-verbs library.

%package fuse
Summary:          Fuse client
Group:            Applications/File
Requires:         %{name} = %{version}-%{release}
Obsoletes:        %{name}-client < 3.1.0
Provides:         %{name}-client = %{version}-%{release}

%description fuse
GlusterFS is a clustered file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides support to FUSE based clients.

%package server
Summary:          Clustered file-system server
Group:            System Environment/Daemons
Requires:         %{name} = %{version}-%{release}

%description server
GlusterFS is a clustered file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the glusterfs server daemon.

%package vim
Summary:        Vim syntax file
Group:          Applications/Text
Requires:       vim-common

%description vim
GlusterFS is a clustered file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

Vim syntax file for GlusterFS.

%package devel
Summary:        Development Libraries
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
GlusterFS is a clustered file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the development libraries.

%prep
%setup -q

%build
%configure

# Remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{__make} %{?_smp_mflags}

%install
%{__make} install DESTDIR=%{buildroot}

# We'll use our init.d
%{__rm} -f %{buildroot}%{_sysconfdir}/init.d/glusterd

# Install include directory
%{__mkdir_p} %{buildroot}%{_includedir}/glusterfs
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/glusterd
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/glusterfs
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/glusterfsd
%{__install} -p -m 0644 libglusterfs/src/*.h \
    %{buildroot}%{_includedir}/glusterfs/

# Remove unwanted files from all the shared libraries
find %{buildroot}%{_libdir} -name '*.a' -delete
find %{buildroot}%{_libdir} -name '*.la' -delete

# Remove installed docs, we include them ourselves as %%doc
%{__rm} -rf %{buildroot}%{_datadir}/doc/glusterfs/

# Rename the samples, so we can include them as %%config
for file in %{buildroot}%{_sysconfdir}/glusterfs/*.sample; do
  %{__mv} ${file} `dirname ${file}`/`basename ${file} .sample`
done

# Create working directory
%{__mkdir_p} %{buildroot}%{_sharedstatedir}/glusterd

# Update configuration file to /var/lib working directory
sed -i 's|option working-directory /etc/glusterd|option working-directory %{_sharedstatedir}/glusterd|g' \
    %{buildroot}%{_sysconfdir}/glusterfs/glusterd.vol

# Clean up the examples we want to include as %%doc
%{__cp} -a doc/examples examples
%{__rm} -f examples/Makefile*

# Install init script and sysconfig file
%{__install} -D -p -m 0755 %{SOURCE1} \
    %{buildroot}%{_initddir}/glusterd
%{__install} -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/sysconfig/glusterd
# Legacy init script and sysconfig file
%{__install} -D -p -m 0755 %{SOURCE11} \
    %{buildroot}%{_initddir}/glusterfsd
%{__install} -D -p -m 0644 %{SOURCE12} \
    %{buildroot}%{_sysconfdir}/sysconfig/glusterfsd

# Install wrapper umount script
%{__install} -D -p -m 0755 %{SOURCE3} \
    %{buildroot}/sbin/umount.glusterfs
# Client logrotate entry
%{__install} -D -p -m 0644 %{SOURCE4} \
    %{buildroot}%{_sysconfdir}/logrotate.d/glusterfs-fuse

# Server logrotate entry
%{__install} -D -p -m 0644 %{SOURCE5} \
    %{buildroot}%{_sysconfdir}/logrotate.d/glusterd
# Legacy server logrotate entry
%{__install} -D -p -m 0644 %{SOURCE15} \
    %{buildroot}%{_sysconfdir}/logrotate.d/glusterfsd

# Install vim syntax plugin
%{__install} -D -p -m 644 extras/glusterfs.vim \
    %{buildroot}%{_datadir}/vim/vimfiles/syntax/glusterfs.vim

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING INSTALL README THANKS
%config(noreplace) %{_sysconfdir}/logrotate.d/glusterd
%config(noreplace) %{_sysconfdir}/sysconfig/glusterd
%if 0%{?_with_fusermount:1}
%{_bindir}/fusermount-glusterfs
%endif
%{_datadir}/glusterfs
%{_bindir}/glusterfs-volgen
%{_libdir}/glusterfs
%{_libdir}/*.so.*
%{_sbindir}/glusterfs*
%{_bindir}/glusterfs-defrag
%{_sbindir}/gluster
%{_sbindir}/glusterd
%{_mandir}/man8/*glusterfs.8*
%{_mandir}/man8/*gluster.8*
%{_mandir}/man8/*glusterd.8*
%{_mandir}/man8/*glusterfs-volgen.8*
%dir %{_localstatedir}/log/glusterfs
%exclude %{_libdir}/glusterfs/%{version}/rpc-transport/rdma*
%exclude %{_libdir}/glusterfs/%{version}/xlator/mount/fuse*

%files rdma
%defattr(-,root,root,-)
%{_libdir}/glusterfs/%{version}/rpc-transport/rdma*

%files fuse
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/logrotate.d/glusterfs-fuse
%{_libdir}/glusterfs/%{version}/xlator/mount/fuse*
%{_mandir}/man8/mount.glusterfs.8*
/sbin/mount.glusterfs
/sbin/umount.glusterfs

%files server
%doc examples/ doc/glusterfs*.vol.sample
%config(noreplace) %{_sysconfdir}/logrotate.d/glusterd
%config(noreplace) %{_sysconfdir}/sysconfig/glusterd
%config(noreplace) %{_sysconfdir}/glusterfs
# Legacy configs
%config(noreplace) %{_sysconfdir}/logrotate.d/glusterfsd
%config(noreplace) %{_sysconfdir}/sysconfig/glusterfsd
%{_localstatedir}/lib/glusterd
%{_initddir}/glusterd
# Legacy init
%{_initddir}/glusterfsd

%files vim
%defattr(-,root,root,-)
%doc COPYING
%{_datadir}/vim/vimfiles/syntax/glusterfs.vim

%files devel
%{_includedir}/glusterfs
%exclude %{_includedir}/glusterfs/y.tab.h
%{_libdir}/*.so

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post server
/sbin/chkconfig --add glusterd

# Legacy server
/sbin/chkconfig --add glusterfsd

%preun server
if [ $1 -eq 0 ]; then
    /sbin/service glusterd stop &>/dev/null || :
    /sbin/chkconfig --del glusterd
fi
if [ $1 -ge 1 ]; then
    /sbin/service glusterd condrestart &>/dev/null || :
fi

# Legacy server
if [ $1 -eq 0 ]; then
    /sbin/service glusterfsd stop &>/dev/null || :
    /sbin/chkconfig --del glusterfsd
fi
if [ $1 -ge 1 ]; then
    /sbin/service glusterfsd condrestart &>/dev/null || :
fi

%changelog
* Mon Dec 27 2010 Silas Sewell <silas@sewell.ch> - 3.1.1-1
- Update to 3.1.1
- Change package names to mirror upstream

* Mon Dec 20 2010 Jonathan Steffan <jsteffan@fedoraproject.org> - 3.0.7-1
- Update to 3.0.7

* Wed Jul 28 2010 Jonathan Steffan <jsteffan@fedoraproject.org> - 3.0.5-1
- Update to 3.0.x

* Sat Apr 10 2010 Jonathan Steffan <jsteffan@fedoraproject.org> - 2.0.9-2
- Move python version requires into a proper BuildRequires otherwise
  the spec always turned off python bindings as python is not part
  of buildsys-build and the chroot will never have python unless we
  require it
- Temporarily set -D_FORTIFY_SOURCE=1 until upstream fixes code
  GlusterFS Bugzilla #197 (#555728)
- Move glusterfs-volgen to devel subpackage (#555724)
- Update description (#554947)

* Sat Jan 2 2010 Jonathan Steffan <jsteffan@fedoraproject.org> - 2.0.9-1
- Update to 2.0.9

* Sat Nov 8 2009 Jonathan Steffan <jsteffan@fedoraproject.org> - 2.0.8-1
- Update to 2.0.8
- Remove install of glusterfs-volgen, it's properly added to
  automake upstream now

* Sat Oct 31 2009 Jonathan Steffan <jsteffan@fedoraproject.org> - 2.0.7-1
- Update to 2.0.7
- Install glusterfs-volgen, until it's properly added to automake
  by upstream
- Add macro to be able to ship more docs

* Thu Sep 17 2009 Peter Lemenkov <lemenkov@gmail.com> 2.0.6-2
- Rebuilt with new fuse

* Sat Sep 12 2009 Matthias Saou <http://freshrpms.net/> 2.0.6-1
- Update to 2.0.6.
- No longer default to disable the client on RHEL5 (#522192).
- Update spec file URLs.

* Mon Jul 27 2009 Matthias Saou <http://freshrpms.net/> 2.0.4-1
- Update to 2.0.4.

* Thu Jun 11 2009 Matthias Saou <http://freshrpms.net/> 2.0.1-2
- Remove libglusterfs/src/y.tab.c to fix koji F11/devel builds.

* Sat May 16 2009 Matthias Saou <http://freshrpms.net/> 2.0.1-1
- Update to 2.0.1.

* Thu May  7 2009 Matthias Saou <http://freshrpms.net/> 2.0.0-1
- Update to 2.0.0 final.

* Wed Apr 29 2009 Matthias Saou <http://freshrpms.net/> 2.0.0-0.3.rc8
- Move glusterfsd to common, since the client has a symlink to it.

* Fri Apr 24 2009 Matthias Saou <http://freshrpms.net/> 2.0.0-0.2.rc8
- Update to 2.0.0rc8.

* Sun Apr 12 2009 Matthias Saou <http://freshrpms.net/> 2.0.0-0.2.rc7
- Update glusterfsd init script to the new style init.
- Update files to match the new default vol file names.
- Include logrotate for glusterfsd, use a pid file by default.
- Include logrotate for glusterfs, using killall for lack of anything better.

* Sat Apr 11 2009 Matthias Saou <http://freshrpms.net/> 2.0.0-0.1.rc7
- Update to 2.0.0rc7.
- Rename "libs" to "common" and move the binary, man page and log dir there.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Matthias Saou <http://freshrpms.net/> 2.0.0-0.1.rc1
- Update to 2.0.0rc1.
- Include new libglusterfsclient.h.

* Mon Feb 16 2009 Matthias Saou <http://freshrpms.net/> 1.3.12-1
- Update to 1.3.12.
- Remove no longer needed ocreat patch.

* Thu Jul 17 2008 Matthias Saou <http://freshrpms.net/> 1.3.10-1
- Update to 1.3.10.
- Remove mount patch, it's been included upstream now.

* Fri May 16 2008 Matthias Saou <http://freshrpms.net/> 1.3.9-1
- Update to 1.3.9.

* Fri May  9 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-1
- Update to 1.3.8 final.

* Tue Apr 23 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.10
- Include short patch to include fixes from latest TLA 751.

* Mon Apr 22 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.9
- Update to 1.3.8pre6.
- Include glusterfs binary in both the client and server packages, now that
  glusterfsd is a symlink to it instead of a separate binary.

* Sun Feb  3 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.8
- Add python version check and disable bindings for version < 2.4.

* Sun Feb  3 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.7
- Add --without client rpmbuild option, make it the default for RHEL (no fuse).
  (I hope "rhel" is the proper default macro name, couldn't find it...)

* Wed Jan 30 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.6
- Add --without ibverbs rpmbuild option to the package.

* Mon Jan 14 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.5
- Update to current TLA again, patch-636 which fixes the known segfaults.

* Thu Jan 10 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.4
- Downgrade to glusterfs--mainline--2.5--patch-628 which is more stable.

* Tue Jan  8 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.3
- Update to current TLA snapshot.
- Include umount.glusterfs wrapper script (really needed? dunno).
- Include patch to mount wrapper to avoid multiple identical mounts.

* Sun Dec 30 2007 Matthias Saou <http://freshrpms.net/> 1.3.8-0.1
- Update to current TLA snapshot, which includes "volume-name=" fstab option.

* Mon Dec  3 2007 Matthias Saou <http://freshrpms.net/> 1.3.7-6
- Re-add the /var/log/glusterfs directory in the client sub-package (required).
- Include custom patch to support vol= in fstab for -n glusterfs client option.

* Mon Nov 26 2007 Matthias Saou <http://freshrpms.net/> 1.3.7-4
- Re-enable libibverbs.
- Check and update License field to GPLv3+.
- Add glusterfs-common obsoletes, to provide upgrade path from old packages.
- Include patch to add mode to O_CREATE opens.

* Thu Nov 22 2007 Matthias Saou <http://freshrpms.net/> 1.3.7-3
- Remove Makefile* files from examples.
- Include RHEL/Fedora type init script, since the included ones don't do.

* Wed Nov 21 2007 Matthias Saou <http://freshrpms.net/> 1.3.7-1
- Major spec file cleanup.
- Add misssing %%clean section.
- Fix ldconfig calls (weren't set for the proper sub-package).

* Sat Aug 4 2007 Matt Paine <matt@mattsoftware.com> - 1.3.pre7
- Added support to build rpm without ibverbs support (use --without ibverbs
  switch)

* Sun Jul 15 2007 Matt Paine <matt@mattsoftware.com> - 1.3.pre6
- Initial spec file
