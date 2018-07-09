#include <pybind11/pybind11.h>
#include <mecab.h>

namespace py = pybind11;

void initialize_path(py::module &m) {
  py::class_<MeCab::Path>(m, "Path")
    .def_readwrite("rnode", &MeCab::Path::rnode)
    .def_readwrite("rnext", &MeCab::Path::rnext)
    .def_readwrite("lnode", &MeCab::Path::lnode)
    .def_readwrite("lnext", &MeCab::Path::lnext)
    .def_readwrite("cost", &MeCab::Path::cost)
    .def_readwrite("prob", &MeCab::Path::prob)
  ;
}