#include <pybind11/pybind11.h>
#include <mecab.h>

#include <memory>

namespace py = pybind11;

void initialize_tagger(py::module &m) {
  // Reference: https://taku910.github.io/mecab/doxygen/index.html
  py::class_<MeCab::Tagger>(m, "Tagger")
    .def(py::init([](const char *argument) {
      return std::unique_ptr<MeCab::Tagger>(MeCab::Tagger::create(argument));
    }))
    .def("parse", [](MeCab::Tagger &self, MeCab::Lattice *lattice) {
      return self.parse(lattice);
    })
    .def("parse", [](MeCab::Tagger &self, const char *text) {
      return self.parse(text);
    })
    .def("parse_to_node", [](MeCab::Tagger &self, const char *text) {
      return self.parseToNode(text);
    }, py::return_value_policy::reference)
    .def("set_theta", [](MeCab::Tagger &self, float theta) {
      self.set_theta(theta);
    })
    .def("theta", [](MeCab::Tagger &self) {
      return self.theta();
    })
    .def("dictionary_info", [](MeCab::Tagger &self) {
      return self.dictionary_info();
    }, py::return_value_policy::reference)
    .def("what", [](MeCab::Tagger &self) {
      return self.what();
    })
    .def("version", [](MeCab::Tagger &self) {
      return MeCab::Tagger::version();
    })
  ;
}