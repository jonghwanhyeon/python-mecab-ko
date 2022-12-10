#include <mecab.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

void initialize_path(py::module &m) {
  // Reference: https://taku910.github.io/mecab/doxygen/structmecab__path__t.html
  py::class_<MeCab::Path>(m, "Path")
      .def_readwrite("rnode", &MeCab::Path::rnode, py::return_value_policy::reference)
      .def_readwrite("rnext", &MeCab::Path::rnext, py::return_value_policy::reference)
      .def_readwrite("lnode", &MeCab::Path::lnode, py::return_value_policy::reference)
      .def_readwrite("lnext", &MeCab::Path::lnext, py::return_value_policy::reference)
      .def_readwrite("cost", &MeCab::Path::cost)
      .def_readwrite("prob", &MeCab::Path::prob);
}