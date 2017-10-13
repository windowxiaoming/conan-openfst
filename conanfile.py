import os
from conans import ConanFile, AutoToolsBuildEnvironment
from conans.tools import download
from conans.tools import untargz
from conans.tools import cpu_count
from conans.tools import patch, environment_append

class OpenFSTConan(ConanFile):
    name = "OpenFST"
    version = "1.6.1"
    license = "Apache 2.0"

    generators = "cmake"
    settings = { "os": ["Linux"],
                 "compiler": {"gcc": {"libcxx": ["libstdc++11"], "version": None},
                              "clang": {"libcxx": ["libstdc++11"], "version": None}},
                 "arch": ["x86_64"],
                 "build_type": ["Debug", "Release"]}
    default_settings = ("os=Linux", "compiler=gcc",
                        "compiler.libcxx=libstdc++11", "arch=x86_64")
    options = {"static": [True, False],
               "shared": [True, False],
               "far": [True, False],
               "ngram_fsts": [True, False]}
    default_options = "static=True", "shared=True", "far=True", "ngram_fsts=True"

    url = "https://github.com/laeknaromur/conan-openfst"
    source_url = "http://openfst.cs.nyu.edu/twiki/pub/FST/FstDownload/openfst-{version}.tar.gz".format(version=version)
    unzipped_path = "openfst-{}".format(version)

    def source(self):
        self.targz_name = os.path.basename(self.source_url)
        download(self.source_url, self.targz_name)
        untargz(self.targz_name)
        os.unlink(self.targz_name)

    def build(self):
        configure_opts = "--prefix={} ".format(self.package_folder)
        if self.options.static:
            configure_opts += " --enable-static "
        if self.options.shared:
            configure_opts += " --enable-shared "
        if self.options.far:
            configure_opts += " --enable-far "
        if self.options.ngram_fsts:
            configure_opts += "--enable-ngram-fsts "
        configure_opts += ' LIBS=\"-ldl\" '

        env_build = AutoToolsBuildEnvironment(self)
        with environment_append(env_build.vars):
            self.run("{}/{}/configure {} ".format(self.conanfile_directory,
                                                  self.unzipped_path,
                                                  configure_opts))
            self.run("make -j{} install".format(cpu_count()))

    def package(self):
        self.copy("*.h", dst="include/fst", src="include/fst")
        self.copy("*.lib", dst="lib", src="lib")
        self.copy("*.la", dst="lib", src="lib")
        self.copy("*.so*", dst="lib", src="lib")
        self.copy("*.a", dst="lib", src="lib")

    def package_info(self):
        self.cpp_info.libs = ["fst", "dl"]
