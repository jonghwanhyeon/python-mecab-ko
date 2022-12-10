#include <memory>
#include <string>
#include <vector>

#include <mecab.h>
#include <pybind11/pybind11.h>

#include "utils.h"

namespace py = pybind11;

void initialize_tagger(py::module &m) {
  // Reference: https://taku910.github.io/mecab/doxygen/classMeCab_1_1Tagger.html
  py::class_<MeCab::Tagger>(m, "Tagger")
      .def(py::init([](const std::vector<std::string> &arguments) {
        std::vector<char *> argv = to_argv(arguments);
        MeCab::Tagger *tagger = MeCab::Tagger::create(argv.size(), argv.data());
        if (tagger == nullptr) {
          throw pybind11::value_error(MeCab::getLastError());
        }

        return std::unique_ptr<MeCab::Tagger>(tagger);
      }))
      .def("parse", py::overload_cast<const char *>(&MeCab::Tagger::parse), py::return_value_policy::reference)
      .def("parse", py::overload_cast<MeCab::Lattice *>(&MeCab::Tagger::parse, py::const_))
      .def("set_theta", &MeCab::Tagger::set_theta)
      .def("theta", &MeCab::Tagger::theta)
      .def("dictionary_info", &MeCab::Tagger::dictionary_info, py::return_value_policy::reference)
      .def("what", &MeCab::Tagger::what, py::return_value_policy::copy)
      .def_static("version", &MeCab::Tagger::version);
}