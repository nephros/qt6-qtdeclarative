%global  qt_version 6.7.2
%define _lto_cflags %{nil}

Summary: Qt6 - QtDeclarative component
Name:    qt6-qtdeclarative
Version: 6.8.3
Release: 0%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io

Source0: %{name}-%{version}.tar.bz2

# filter qml provides
%global __provides_exclude_from ^%{_qt6_qmldir}/.*\\.so$

BuildRequires: cmake
BuildRequires: clang
BuildRequires: ninja
BuildRequires: qt6-rpm-macros
BuildRequires: qt6-qtbase-devel >= %{qt_version}
BuildRequires: qt6-qtbase-private-devel
BuildRequires: qt6-qtbase-static
BuildRequires: qt6-qtlanguageserver-devel >= %{qt_version}
BuildRequires: qt6-qtshadertools-devel >= %{qt_version}
BuildRequires: qt6-qtsvg-devel >= %{qt_version}
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: python3-base
BuildRequires: pkgconfig(xkbcommon) >= 0.4.1

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Provides:  %{name}-private-devel = %{version}-%{release}
Requires:  %{name}%{?_isa} = %{version}-%{release}
Requires:  qt6-qtbase-devel%{?_isa}
Obsoletes: qt6-qtquickcontrols2-devel < 6.2.0~beta3-1
Provides:  qt6-qtquickcontrols2-devel = %{version}-%{release}
%description devel
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%description static
%{summary}.

%prep
%autosetup -n %{name}-%{version}/upstream -p1


%build

# HACK so calls to "python" get what we want
ln -s %{__python3} python
export PATH=`pwd`:$PATH

%cmake_qt6 \
  -DQT_BUILD_EXAMPLES:BOOL=OFF \
  -DQT_INSTALL_EXAMPLES_SOURCES=OFF \
  %{nil}

%cmake_build


%install
%cmake_install

# hardlink files to %{_bindir}, add -qt6 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt6_bindir}
for i in * ; do
  case "${i}" in
    qmlcachegen|qmlleasing|qmlformat|qmleasing|qmlimportscanner|qmllint| \
    qmlpreview|qmlscene|qmltestrunner|qmltyperegistrar|qmlplugindump| \
    qmlprofiler|qml|qmlbundle|qmlmin|qmltime)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt6
      ;;
    *)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
      ;;
  esac
done
popd

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  rm -fv "$(basename ${prl_file} .prl).la"
  sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSES/LGPL*
#%%{_qt6_archdatadir}/sbom/%%{qt_module}-%%{qt_version}.spdx
%{_qt6_libdir}/libQt6LabsAnimation.so.6*
%{_qt6_libdir}/libQt6LabsFolderListModel.so.6*
%{_qt6_libdir}/libQt6LabsPlatform.so.6*
%{_qt6_libdir}/libQt6LabsQmlModels.so.6*
%{_qt6_libdir}/libQt6LabsSettings.so.6*
%{_qt6_libdir}/libQt6LabsSharedImage.so.6*
%{_qt6_libdir}/libQt6LabsWavefrontMesh.so.6*
%{_qt6_libdir}/libQt6Qml.so.6*
%{_qt6_libdir}/libQt6QmlCompiler.so.*
%{_qt6_libdir}/libQt6QmlCore.so.6*
%{_qt6_libdir}/libQt6QmlLocalStorage.so.6*
%{_qt6_libdir}/libQt6QmlMeta.so.6*
%{_qt6_libdir}/libQt6QmlModels.so.6*
%{_qt6_libdir}/libQt6QmlNetwork.so.6*
%{_qt6_libdir}/libQt6QmlWorkerScript.so.6*
%{_qt6_libdir}/libQt6QmlXmlListModel.so.6*
%{_qt6_libdir}/libQt6Quick.so.6*
%{_qt6_libdir}/libQt6QuickControls2.so.6*
%{_qt6_libdir}/libQt6QuickControls2Basic.so.6*
%{_qt6_libdir}/libQt6QuickControls2BasicStyleImpl.so.6*
%{_qt6_libdir}/libQt6QuickControls2FluentWinUI3StyleImpl.so.6*
%{_qt6_libdir}/libQt6QuickControls2Fusion.so.6*
%{_qt6_libdir}/libQt6QuickControls2FusionStyleImpl.so.6*
%{_qt6_libdir}/libQt6QuickControls2Imagine.so.6*
%{_qt6_libdir}/libQt6QuickControls2ImagineStyleImpl.so.6*
%{_qt6_libdir}/libQt6QuickControls2Impl.so.6*
%{_qt6_libdir}/libQt6QuickControls2Material.so.6*
%{_qt6_libdir}/libQt6QuickControls2MaterialStyleImpl.so.6*
%{_qt6_libdir}/libQt6QuickControls2Universal.so.6*
%{_qt6_libdir}/libQt6QuickControls2UniversalStyleImpl.so.6*
%{_qt6_libdir}/libQt6QuickDialogs2.so.6*
%{_qt6_libdir}/libQt6QuickDialogs2QuickImpl.so.6*
%{_qt6_libdir}/libQt6QuickDialogs2Utils.so.6*
%{_qt6_libdir}/libQt6QuickEffects.so.6*
%{_qt6_libdir}/libQt6QuickLayouts.so.6*
%{_qt6_libdir}/libQt6QuickParticles.so.6*
%{_qt6_libdir}/libQt6QuickShapes.so.6*
%{_qt6_libdir}/libQt6QuickTemplates2.so.6*
%{_qt6_libdir}/libQt6QuickTest.so.6*
%{_qt6_libdir}/libQt6QuickVectorImage.so.6*
%{_qt6_libdir}/libQt6QuickVectorImageGenerator.so.6*
%{_qt6_libdir}/libQt6QuickWidgets.so.6*
%{_qt6_plugindir}/qmltooling/
%{_qt6_plugindir}/qmllint/
%{_qt6_plugindir}/qmlls/
%dir %{_qt6_qmldir}
%{_qt6_qmldir}/QML/
%{_qt6_qmldir}/QmlTime/
%{_qt6_qmldir}/Qt/
%{_qt6_qmldir}/QtCore/
%{_qt6_qmldir}/QtNetwork/
%{_qt6_qmldir}/QtQml/
%{_qt6_qmldir}/QtQuick/
%{_qt6_qmldir}/QtTest/
%{_qt6_qmldir}/builtins.qmltypes
%{_qt6_qmldir}/jsroot.qmltypes

%files devel
%dir %{_qt6_libdir}/cmake/Qt6LabsAnimation
%dir %{_qt6_libdir}/cmake/Qt6LabsFolderListModel
%dir %{_qt6_libdir}/cmake/Qt6LabsPlatform
%dir %{_qt6_libdir}/cmake/Qt6LabsQmlModels
%dir %{_qt6_libdir}/cmake/Qt6LabsSettings
%dir %{_qt6_libdir}/cmake/Qt6LabsSharedImage
%dir %{_qt6_libdir}/cmake/Qt6LabsWavefrontMesh
%dir %{_qt6_libdir}/cmake/Qt6Qml
%dir %{_qt6_libdir}/cmake/Qt6QmlCompiler
%dir %{_qt6_libdir}/cmake/Qt6QmlCore
%dir %{_qt6_libdir}/cmake/Qt6QmlImportScanner
%dir %{_qt6_libdir}/cmake/Qt6QmlIntegration
%dir %{_qt6_libdir}/cmake/Qt6QmlLocalStorage
%dir %{_qt6_libdir}/cmake/Qt6QmlMeta
%dir %{_qt6_libdir}/cmake/Qt6QmlModels
%dir %{_qt6_libdir}/cmake/Qt6QmlNetwork
%dir %{_qt6_libdir}/cmake/Qt6QmlTools
%dir %{_qt6_libdir}/cmake/Qt6QmlWorkerScript
%dir %{_qt6_libdir}/cmake/Qt6QmlXmlListModel
%dir %{_qt6_libdir}/cmake/Qt6Quick
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Basic
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2BasicStyleImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2FluentWinUI3StyleImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Fusion
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2FusionStyleImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Imagine
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2ImagineStyleImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Impl
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Material
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2MaterialStyleImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Universal
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2UniversalStyleImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickDialogs2
%dir %{_qt6_libdir}/cmake/Qt6QuickDialogs2QuickImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickDialogs2Utils
%dir %{_qt6_libdir}/cmake/Qt6QuickLayouts
%dir %{_qt6_libdir}/cmake/Qt6QuickTemplates2
%dir %{_qt6_libdir}/cmake/Qt6QuickTest
%dir %{_qt6_libdir}/cmake/Qt6QuickTools
%dir %{_qt6_libdir}/cmake/Qt6QuickVectorImage
%dir %{_qt6_libdir}/cmake/Qt6QuickWidgets
%{_bindir}/qml*
%{_bindir}/svgtoqml
%{_qt6_bindir}/qml*
%{_qt6_bindir}/svgtoqml
%{_qt6_libexecdir}/qmlcachegen
%{_qt6_libexecdir}/qmlimportscanner
%{_qt6_libexecdir}/qmltyperegistrar
%{_qt6_libexecdir}/qmljsrootgen
%{_qt6_libexecdir}/qmlaotstats
%{_qt6_headerdir}/QtLabs*/
%{_qt6_headerdir}/QtQml/
%{_qt6_headerdir}/QtQmlCompiler/
%{_qt6_headerdir}/QtQmlCore/
%{_qt6_headerdir}/QtQmlIntegration/
%{_qt6_headerdir}/QtQmlLocalStorage/
%{_qt6_headerdir}/QtQmlMeta/
%{_qt6_headerdir}/QtQmlModels/
%{_qt6_headerdir}/QtQmlNetwork/
%{_qt6_headerdir}/QtQmlWorkerScript/
%{_qt6_headerdir}/QtQmlXmlListModel/
%{_qt6_headerdir}/QtQuick/
%{_qt6_headerdir}/QtQuickControls2*StyleImpl/
%{_qt6_headerdir}/QtQuickControls2/
%{_qt6_headerdir}/QtQuickControls2Basic/
%{_qt6_headerdir}/QtQuickControls2Fusion/
%{_qt6_headerdir}/QtQuickControls2Imagine/
%{_qt6_headerdir}/QtQuickControls2Impl/
%{_qt6_headerdir}/QtQuickControls2Material/
%{_qt6_headerdir}/QtQuickControls2Universal/
%{_qt6_headerdir}/QtQuickDialogs2/
%{_qt6_headerdir}/QtQuickDialogs2QuickImpl/
%{_qt6_headerdir}/QtQuickDialogs2Utils/
%{_qt6_headerdir}/QtQuickEffects/
%{_qt6_headerdir}/QtQuickLayouts/
%{_qt6_headerdir}/QtQuickParticles/
%{_qt6_headerdir}/QtQuickShapes/
%{_qt6_headerdir}/QtQuickTemplates2/
%{_qt6_headerdir}/QtQuickTest/
%{_qt6_headerdir}/QtQuickVectorImage/
%{_qt6_headerdir}/QtQuickVectorImageGenerator/
%{_qt6_headerdir}/QtQuickWidgets/
%{_qt6_libdir}/libQt6Labs*.prl
%{_qt6_libdir}/libQt6Labs*.so
%{_qt6_libdir}/libQt6Qml.prl
%{_qt6_libdir}/libQt6Qml.so
%{_qt6_libdir}/libQt6QmlCompiler.prl
%{_qt6_libdir}/libQt6QmlCompiler.so
%{_qt6_libdir}/libQt6QmlCore.prl
%{_qt6_libdir}/libQt6QmlCore.so
%{_qt6_libdir}/libQt6QmlLocalStorage.prl
%{_qt6_libdir}/libQt6QmlLocalStorage.so
%{_qt6_libdir}/libQt6QmlMeta.prl
%{_qt6_libdir}/libQt6QmlMeta.so
%{_qt6_libdir}/libQt6QmlModels.prl
%{_qt6_libdir}/libQt6QmlModels.so
%{_qt6_libdir}/libQt6QmlNetwork.prl
%{_qt6_libdir}/libQt6QmlNetwork.so
%{_qt6_libdir}/libQt6QmlWorkerScript.prl
%{_qt6_libdir}/libQt6QmlWorkerScript.so
%{_qt6_libdir}/libQt6QmlXmlListModel.prl
%{_qt6_libdir}/libQt6QmlXmlListModel.so
%{_qt6_libdir}/libQt6Quick*Impl.prl
%{_qt6_libdir}/libQt6Quick*Impl.so
%{_qt6_libdir}/libQt6Quick.prl
%{_qt6_libdir}/libQt6Quick.so
%{_qt6_libdir}/libQt6QuickControls2.prl
%{_qt6_libdir}/libQt6QuickControls2.so
%{_qt6_libdir}/libQt6QuickControls2Basic.prl
%{_qt6_libdir}/libQt6QuickControls2Basic.so
%{_qt6_libdir}/libQt6QuickControls2Fusion.prl
%{_qt6_libdir}/libQt6QuickControls2Fusion.so
%{_qt6_libdir}/libQt6QuickControls2Imagine.prl
%{_qt6_libdir}/libQt6QuickControls2Imagine.so
%{_qt6_libdir}/libQt6QuickControls2Material.prl
%{_qt6_libdir}/libQt6QuickControls2Material.so
%{_qt6_libdir}/libQt6QuickControls2Universal.prl
%{_qt6_libdir}/libQt6QuickControls2Universal.so
%{_qt6_libdir}/libQt6QuickDialogs2.prl
%{_qt6_libdir}/libQt6QuickDialogs2.so
%{_qt6_libdir}/libQt6QuickDialogs2Utils.prl
%{_qt6_libdir}/libQt6QuickDialogs2Utils.so
%{_qt6_libdir}/libQt6QuickEffects.prl
%{_qt6_libdir}/libQt6QuickEffects.so
%{_qt6_libdir}/libQt6QuickLayouts.prl
%{_qt6_libdir}/libQt6QuickLayouts.so
%{_qt6_libdir}/libQt6QuickParticles.prl
%{_qt6_libdir}/libQt6QuickParticles.so
%{_qt6_libdir}/libQt6QuickShapes.prl
%{_qt6_libdir}/libQt6QuickShapes.so
%{_qt6_libdir}/libQt6QuickTemplates2.prl
%{_qt6_libdir}/libQt6QuickTemplates2.so
%{_qt6_libdir}/libQt6QuickTest.prl
%{_qt6_libdir}/libQt6QuickTest.so
%{_qt6_libdir}/libQt6QuickVectorImage.prl
%{_qt6_libdir}/libQt6QuickVectorImage.so
%{_qt6_libdir}/libQt6QuickVectorImageGenerator.prl
%{_qt6_libdir}/libQt6QuickVectorImageGenerator.so
%{_qt6_libdir}/libQt6QuickWidgets.prl
%{_qt6_libdir}/libQt6QuickWidgets.so
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtDeclarativeTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6LabsAnimation/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsFolderListModel/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsPlatform/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsQmlModels/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsSettings/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsSharedImage/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsWavefrontMesh/*.cmake
%{_qt6_libdir}/cmake/Qt6Qml/*.cmake*
%{_qt6_libdir}/cmake/Qt6Qml/*.conf.in
%{_qt6_libdir}/cmake/Qt6Qml/*.cpp.in
%{_qt6_libdir}/cmake/Qt6Qml/*.qrc.in
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlCompiler/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlCore/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlImportScanner/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlIntegration/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlLocalStorage/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlMeta/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlModels/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlNetwork/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlTools/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlWorkerScript/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlXmlListModel/*.cmake
%{_qt6_libdir}/cmake/Qt6Quick/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Basic/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2BasicStyleImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2FluentWinUI3StyleImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Fusion/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2FusionStyleImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Imagine/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2ImagineStyleImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Impl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Material/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2MaterialStyleImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Universal/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2UniversalStyleImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickDialogs2/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickDialogs2QuickImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickDialogs2Utils/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickLayouts/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickTemplates2/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickTest/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickTools/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickVectorImage/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickWidgets/*.cmake
%dir %{_qt6_mkspecsdir}/features
%{_qt6_mkspecsdir}/features/qmlcache.prf
%{_qt6_mkspecsdir}/features/qmltypes.prf
%{_qt6_mkspecsdir}/features/qtquickcompiler.prf
%{_qt6_descriptionsdir}/Labs*.json
%{_qt6_descriptionsdir}/Qml.json
%{_qt6_descriptionsdir}/QmlCompiler.json
%{_qt6_descriptionsdir}/QmlCore.json
%{_qt6_descriptionsdir}/QmlIntegration.json
%{_qt6_descriptionsdir}/QmlLocalStorage.json
%{_qt6_descriptionsdir}/QmlMeta.json
%{_qt6_descriptionsdir}/QmlModels.json
%{_qt6_descriptionsdir}/QmlNetwork.json
%{_qt6_descriptionsdir}/QmlWorkerScript.json
%{_qt6_descriptionsdir}/QmlXmlListModel.json
%{_qt6_descriptionsdir}/Quick.json
%{_qt6_descriptionsdir}/QuickControls2*Impl.json
%{_qt6_descriptionsdir}/QuickControls2.json
%{_qt6_descriptionsdir}/QuickControls2Basic.json
%{_qt6_descriptionsdir}/QuickControls2Fusion.json
%{_qt6_descriptionsdir}/QuickControls2Imagine.json
%{_qt6_descriptionsdir}/QuickControls2Material.json
%{_qt6_descriptionsdir}/QuickControls2Universal.json
%{_qt6_descriptionsdir}/QuickDialogs2.json
%{_qt6_descriptionsdir}/QuickDialogs2QuickImpl.json
%{_qt6_descriptionsdir}/QuickDialogs2Utils.json
%{_qt6_descriptionsdir}/QuickLayouts.json
%{_qt6_descriptionsdir}/QuickTemplates2.json
%{_qt6_descriptionsdir}/QuickTest.json
%{_qt6_descriptionsdir}/QuickVectorImage.json
%{_qt6_descriptionsdir}/QuickWidgets.json
%{_qt6_metatypesdir}/qt6labs*_metatypes.json
%{_qt6_metatypesdir}/qt6qml_*_metatypes.json
%{_qt6_metatypesdir}/qt6qmlcompiler_*_metatypes.json
%{_qt6_metatypesdir}/qt6qmlcore_relwithdebinfo_metatypes.json
%{_qt6_metatypesdir}/qt6qmllocalstorage_relwithdebinfo_metatypes.json
%{_qt6_metatypesdir}/qt6qmlmeta_relwithdebinfo_metatypes.json
%{_qt6_metatypesdir}/qt6qmlmodels_relwithdebinfo_metatypes.json
%{_qt6_metatypesdir}/qt6qmlnetwork_relwithdebinfo_metatypes.json
%{_qt6_metatypesdir}/qt6qmlworkerscript_relwithdebinfo_metatypes.json
%{_qt6_metatypesdir}/qt6qmlxmllistmodel_relwithdebinfo_metatypes.json
%{_qt6_metatypesdir}/qt6quick*impl*_metatypes.json
%{_qt6_metatypesdir}/qt6quick_*_metatypes.json
%{_qt6_metatypesdir}/qt6quickcontrols2_*.json
%{_qt6_metatypesdir}/qt6quickcontrols2basic_*_metatypes.json
%{_qt6_metatypesdir}/qt6quickcontrols2fusion_*_metatypes.json
%{_qt6_metatypesdir}/qt6quickcontrols2imagine_*_metatypes.json
%{_qt6_metatypesdir}/qt6quickcontrols2material_*_metatypes.json
%{_qt6_metatypesdir}/qt6quickcontrols2universal_*_metatypes.json
%{_qt6_metatypesdir}/qt6quickdialogs2_*.json
%{_qt6_metatypesdir}/qt6quickdialogs2utils_relwithdebinfo_metatypes.json
%{_qt6_metatypesdir}/qt6quicklayouts_relwithdebinfo_metatypes.json
%{_qt6_metatypesdir}/qt6quicktest_*_metatypes.json
%{_qt6_metatypesdir}/qt6quicktemplates2_relwithdebinfo_metatypes.json
%{_qt6_metatypesdir}/qt6quickvectorimage_relwithdebinfo_metatypes.json
%{_qt6_metatypesdir}/qt6quickwidgets_*_metatypes.json
%{_qt6_mkspecsdir}/modules/qt_lib_labs*.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qml.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmlcompiler.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmlcore.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmlintegration.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmllocalstorage.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmlmeta.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmlmodels.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmlnetwork.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmltest.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmlworkerscript.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmlxmllistmodel.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quick*impl.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quick.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickcontrols2.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickcontrols2basic.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickcontrols2fusion.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickcontrols2imagine.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickcontrols2material.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickcontrols2universal.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickdialogs2.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickdialogs2utils.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quicklayouts.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quicktemplates2.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickvectorimage.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickwidgets.pri
%{_qt6_libdir}/pkgconfig/Qt6Labs*.pc
%{_qt6_libdir}/pkgconfig/Qt6Qml.pc
%{_qt6_libdir}/pkgconfig/Qt6QmlCompiler.pc
%{_qt6_libdir}/pkgconfig/Qt6QmlCore.pc
%{_qt6_libdir}/pkgconfig/Qt6QmlIntegration.pc
%{_qt6_libdir}/pkgconfig/Qt6QmlLocalStorage.pc
%{_qt6_libdir}/pkgconfig/Qt6QmlMeta.pc
%{_qt6_libdir}/pkgconfig/Qt6QmlModels.pc
%{_qt6_libdir}/pkgconfig/Qt6QmlNetwork.pc
%{_qt6_libdir}/pkgconfig/Qt6QmlWorkerScript.pc
%{_qt6_libdir}/pkgconfig/Qt6QmlXmlListModel.pc
%{_qt6_libdir}/pkgconfig/Qt6Quick*Impl.pc
%{_qt6_libdir}/pkgconfig/Qt6Quick.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickControls2.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickControls2Basic.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickControls2Fusion.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickControls2Imagine.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickControls2Material.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickControls2Universal.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickDialogs2.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickDialogs2Utils.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickLayouts.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickTemplates2.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickTest.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickVectorImage.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickWidgets.pc
# FIXME:
# This (slit to -private-devel) didn't work out because of rhbz#2330219
# Might be something to consider in the future.
# Private stuff
# {_qt6_headerdir}/*/{qt_version}
%dir %{_qt6_libdir}/cmake/Qt6QuickEffectsPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickParticlesPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickShapesPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickVectorImageGeneratorPrivate
%{_qt6_libdir}/cmake/Qt6QuickEffectsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickParticlesPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickShapesPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickVectorImageGeneratorPrivate/*.cmake
%{_qt6_descriptionsdir}/QuickEffectsPrivate.json
%{_qt6_descriptionsdir}/QuickParticlesPrivate.json
%{_qt6_descriptionsdir}/QuickShapesPrivate.json
%{_qt6_descriptionsdir}/QuickVectorImageGeneratorPrivate.json
%{_qt6_metatypesdir}/qt6quickeffectsprivate_relwithdebinfo_metatypes.json
%{_qt6_metatypesdir}/qt6quickparticlesprivate_relwithdebinfo_metatypes.json
%{_qt6_metatypesdir}/qt6quickshapesprivate_relwithdebinfo_metatypes.json
%{_qt6_metatypesdir}/qt6quickvectorimagegeneratorprivate_relwithdebinfo_metatypes.json
%{_qt6_mkspecsdir}/modules/qt_lib_*_private.pri

%files static
%dir %{_qt6_archdatadir}/objects-*
%dir %{_qt6_libdir}/cmake/Qt6PacketProtocolPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlDebugPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlDomPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlLSPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlToolingSettingsPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlTypeRegistrarPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickControlsTestUtilsPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickTestUtilsPrivate
%{_qt6_libdir}/cmake/Qt6PacketProtocolPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlDebugPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlDomPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlLSPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlToolingSettingsPrivate/*cmake
%{_qt6_libdir}/cmake/Qt6QmlTypeRegistrarPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControlsTestUtilsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickTestUtilsPrivate/*.cmake
%{_qt6_headerdir}/QtPacketProtocol/
%{_qt6_headerdir}/QtQmlDebug/
%{_qt6_headerdir}/QtQmlDom/
%{_qt6_headerdir}/QtQmlLS/
%{_qt6_headerdir}/QtQmlToolingSettings/
%{_qt6_headerdir}/QtQmlTypeRegistrar/
%{_qt6_headerdir}/QtQuickControlsTestUtils/
%{_qt6_headerdir}/QtQuickTestUtils/
%{_qt6_libdir}/libQt6PacketProtocol.a
%{_qt6_libdir}/libQt6PacketProtocol.prl
%{_qt6_libdir}/libQt6QmlDebug.a
%{_qt6_libdir}/libQt6QmlDebug.prl
%{_qt6_libdir}/libQt6QmlDom.a
%{_qt6_libdir}/libQt6QmlDom.prl
%{_qt6_libdir}/libQt6QmlLS.a
%{_qt6_libdir}/libQt6QmlLS.prl
%{_qt6_libdir}/libQt6QmlToolingSettings.a
%{_qt6_libdir}/libQt6QmlToolingSettings.prl
%{_qt6_libdir}/libQt6QmlTypeRegistrar.a
%{_qt6_libdir}/libQt6QmlTypeRegistrar.prl
%{_qt6_libdir}/libQt6QuickControlsTestUtils.a
%{_qt6_libdir}/libQt6QuickControlsTestUtils.prl
%{_qt6_libdir}/libQt6QuickTestUtils.a
%{_qt6_libdir}/libQt6QuickTestUtils.prl
%{_qt6_descriptionsdir}/PacketProtocolPrivate.json
%{_qt6_descriptionsdir}/QmlDebugPrivate.json
%{_qt6_descriptionsdir}/QmlDomPrivate.json
%{_qt6_descriptionsdir}/QmlLSPrivate.json
%{_qt6_descriptionsdir}/QmlToolingSettingsPrivate.json
%{_qt6_descriptionsdir}/QmlTypeRegistrarPrivate.json
%{_qt6_descriptionsdir}/QuickControlsTestUtilsPrivate.json
%{_qt6_descriptionsdir}/QuickTestUtilsPrivate.json
%{_qt6_metatypesdir}/qt6packetprotocolprivate_*_metatypes.json
%{_qt6_metatypesdir}/qt6qmldebugprivate_*_metatypes.json
%{_qt6_metatypesdir}/qt6qmldomprivate_*_metatypes.json
%{_qt6_metatypesdir}/qt6qmllsprivate_*_metatypes.json
%{_qt6_metatypesdir}/qt6qmltoolingsettingsprivate_*_metatypes.json
%{_qt6_metatypesdir}/qt6qmltyperegistrarprivate_*_metatypes.json
%{_qt6_metatypesdir}/qt6quickcontrolstestutilsprivate_*_metatypes.json
%{_qt6_metatypesdir}/qt6quicktestutilsprivate_*_metatypes.json
# FIXME:
# Same to qtbase, we probably cannot have mkspecs separate from -devel
#{_qt6_mkspecsdir}/modules/qt_lib_packetprotocol_private.pri
#{_qt6_mkspecsdir}/modules/qt_lib_qmldebug_private.pri
#{_qt6_mkspecsdir}/modules/qt_lib_qmldom_private.pri
#{_qt6_mkspecsdir}/modules/qt_lib_qmlls_private.pri
#{_qt6_mkspecsdir}/modules/qt_lib_qmltoolingsettings_private.pri
#{_qt6_mkspecsdir}/modules/qt_lib_qmltyperegistrar_private.pri
#{_qt6_mkspecsdir}/modules/qt_lib_quickcontrolstestutilsprivate_private.pri
#{_qt6_mkspecsdir}/modules/qt_lib_quicktestutilsprivate_private.pri
%{_qt6_archdatadir}/objects-*/QmlTypeRegistrarPrivate_resources_1/


