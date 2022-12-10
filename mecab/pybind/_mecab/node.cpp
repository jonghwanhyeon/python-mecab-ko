#include <sstream>

#include <mecab.h>
#include <pybind11/pybind11.h>

#include "utils.h"

namespace py = pybind11;

void initialize_node(py::module &m) {
  // Parameters for MeCab::Node::stat
  m.attr("MECAB_NOR_NODE") = 0;
  m.attr("MECAB_UNK_NODE") = 1;
  m.attr("MECAB_BOS_NODE") = 2;
  m.attr("MECAB_EOS_NODE") = 3;
  m.attr("MECAB_EON_NODE") = 4;

  // Reference: https://taku910.github.io/mecab/doxygen/structmecab__node__t.html
  py::class_<MeCab::Node>(m, "Node")
      .def_readwrite("prev", &MeCab::Node::prev, py::return_value_policy::reference)
      .def_readwrite("next", &MeCab::Node::next, py::return_value_policy::reference)
      .def_readwrite("enext", &MeCab::Node::enext, py::return_value_policy::reference)
      .def_readwrite("bnext", &MeCab::Node::bnext, py::return_value_policy::reference)
      .def_readwrite("rpath", &MeCab::Node::rpath, py::return_value_policy::reference)
      .def_readwrite("lpath", &MeCab::Node::lpath, py::return_value_policy::reference)
      .def_property_readonly("surface", [](MeCab::Node &self) { return std::string(self.surface, self.length); })
      .def_readonly("feature", &MeCab::Node::feature, py::return_value_policy::reference)
      .def_readwrite("id", &MeCab::Node::id)
      .def_readwrite("length", &MeCab::Node::length)
      .def_readwrite("rlength", &MeCab::Node::rlength)
      .def_readwrite("rc_attr", &MeCab::Node::rcAttr)
      .def_readwrite("lc_attr", &MeCab::Node::lcAttr)
      .def_readwrite("posid", &MeCab::Node::posid)
      .def_readwrite("char_type", &MeCab::Node::char_type)
      .def_readwrite("stat", &MeCab::Node::stat)
      .def_readwrite("isbest", &MeCab::Node::isbest)
      .def_readwrite("alpha", &MeCab::Node::alpha)
      .def_readwrite("beta", &MeCab::Node::beta)
      .def_readwrite("prob", &MeCab::Node::prob)
      .def_readwrite("wcost", &MeCab::Node::wcost)
      .def_readwrite("cost", &MeCab::Node::cost)
      .def("__repr__", [](const MeCab::Node &self) {
        std::stringstream stream;
        stream << "Node(";
        stream << "surface=\"" << escape(std::string(self.surface, self.length)) << "\", ";
        stream << "feature=\"" << escape(self.feature) << "\"";
        stream << ")";
        return stream.str();
      });
}