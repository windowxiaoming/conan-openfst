import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.tools import download
from conans.tools import untargz
from conans.tools import cpu_count
from conans.tools import patch, environment_append

class OpenFSTConan(ConanFile):
    name = "OpenFST"
    version = "1.6.5"
    license = "Apache 2.0"

    generators = "cmake", "virtualbuildenv", "virtualrunenv"
    settings = { "os": ["Linux"],
                 "compiler": {"gcc": {"libcxx": ["libstdc++11"], "version": None},
                              "clang": {"libcxx": ["libstdc++11"], "version": None}},
                 "arch": ["x86_64"],
                 "build_type": ["Debug", "Release"]}
    default_settings = ("os=Linux", "compiler=gcc",
                        "compiler.libcxx=libstdc++11", "arch=x86_64")
    options = {
        "static": [True, False],
        "shared": [True, False],
        "far": [True, False],
        "ngram_fsts": [True, False],
        "const_fsts": [True, False],
        "compact_fsts": [True, False],
        "compress": [True, False],
        "linear_fsts": [True, False],
        "lookahead_fsts": [True, False],
        "python": [True, False],
        "pdt": [True, False],
        "mpdt": [True, False],
        "special": [True, False],
        "bin": [True, False],
    }
    default_options = (
        "static=True",
        "shared=True",
        "far=True",
        "ngram_fsts=True",
        "const_fsts=True",
        "compact_fsts=True",
        "compress=True",
        "linear_fsts=True",
        "lookahead_fsts=True",
        "python=True",
        "pdt=True",
        "mpdt=True",
        "special=True",
        "bin=True"
    )

    url = "https://github.com/laeknaromur/conan-openfst"
    source_url = "http://openfst.org/twiki/pub/FST/FstDownload/openfst-{version}.tar.gz".format(version=version)
    unzipped_path = "openfst-{}".format(version)

    def source(self):
        self.targz_name = os.path.basename(self.source_url)
        download(self.source_url, self.targz_name)
        untargz(self.targz_name)
        os.unlink(self.targz_name)

    def build(self):
        features = [
            "--enable-static={}".format("yes" if self.options.static else "no"),
            "--enable-shared={}".format("yes" if self.options.shared else "no"),
            "--enable-compact-fsts={}".format("yes" if self.options.compact_fsts else "no"),
            "--enable-compress={}".format("yes" if self.options.compress else "no"),
            "--enable-const-fsts={}".format("yes" if self.options.const_fsts else "no"),
            "--enable-far={}".format("yes" if self.options.far else "no"),
            "--enable-linear-fsts={}".format("yes" if self.options.linear_fsts else "no"),
            "--enable-lookahead-fsts={}".format("yes" if self.options.lookahead_fsts else "no"),
            "--enable-mpdt={}".format("yes" if self.options.mpdt else "no"),
            "--enable-ngram-fsts={}".format("yes" if self.options.ngram_fsts else "no"),
            "--enable-pdt={}".format("yes" if self.options.pdt else "no"),
            "--enable-python={}".format("yes" if self.options.python else "no"),
            "--enable-special={}".format("yes" if self.options.special else "no"),
            "--enable-bin={}".format("yes" if self.options.bin else "no")
        ]
        configure_opts = "--prefix={} ".format(self.package_folder)
        configure_opts += ' LIBS=\"-ldl\" '
        configure_opts += ' '.join(features)

        env_build = AutoToolsBuildEnvironment(self)
        with environment_append(env_build.vars):
            self.run("{}/configure {} ".format(self.unzipped_path,
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
