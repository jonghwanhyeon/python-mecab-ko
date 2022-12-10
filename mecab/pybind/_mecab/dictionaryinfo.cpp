#include <mecab.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

void initialize_dictionaryinfo(py::module &m) {
  // Parameters for MeCab::DictionaryInfo::type
  m.attr("MECAB_SYS_DIC") = 0;
  m.attr("MECAB_USR_DIC") = 1;
  m.attr("MECAB_UNK_DIC") = 2;

  // Reference: https://taku910.github.io/mecab/doxygen/structmecab__dictionary__info__t.html
  py::class_<MeCab::DictionaryInfo>(m, "DictionaryInfo")
      .def_readonly("filename", &MeCab::DictionaryInfo::filename)
      .def_readonly("charset", &MeCab::DictionaryInfo::charset)
      .def_readwrite("size", &MeCab::DictionaryInfo::size)
      .def_readwrite("type", &MeCab::DictionaryInfo::type)
      .def_readwrite("lsize", &MeCab::DictionaryInfo::lsize)
      .def_readwrite("rsize", &MeCab::DictionaryInfo::rsize)
      .def_readwrite("version", &MeCab::DictionaryInfo::version)
      .def_readwrite("next", &MeCab::DictionaryInfo::next);
}