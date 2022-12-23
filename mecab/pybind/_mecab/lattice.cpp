#include <sstream>

#include <mecab.h>
#include <pybind11/pybind11.h>

#include "utils.h"

namespace py = pybind11;

typedef std::tuple<size_t, size_t> Span;

class Iterator {
private:
  const MeCab::Node *cursor;
  const char *sentence;

public:
  explicit Iterator(const MeCab::Node *cursor) : cursor(cursor), sentence(cursor->surface) {}

  const std::tuple<const Span, const MeCab::Node &> operator*() const {
    size_t offset = cursor->surface - sentence;

    return std::make_tuple(
        Span{utf8_strlen(sentence, sentence + offset), utf8_strlen(sentence, sentence + offset + cursor->length)},
        std::cref(*cursor));
  }

  Iterator &operator++() {
    cursor = cursor->next;
    return *this;
  }

  bool operator==(const Iterator &rhs) const { return cursor == rhs.cursor; }
};

void initialize_lattice(py::module &m) {
  // Parameters for MeCab::Lattice::request_type
  m.attr("MECAB_ONE_BEST") = 1;
  m.attr("MECAB_NBEST") = 2;
  m.attr("MECAB_PARTIAL") = 4;
  m.attr("MECAB_MARGINAL_PROB") = 8;
  m.attr("MECAB_ALTERNATIVE") = 16;
  m.attr("MECAB_ALL_MORPHS") = 32;
  m.attr("MECAB_ALLOCATE_SENTENCE") = 64;

  // Parameters for MeCab::Lattice::boundary_constraint_type
  m.attr("MECAB_ANY_BOUNDARY") = 0;
  m.attr("MECAB_TOKEN_BOUNDARY") = 1;
  m.attr("MECAB_INSIDE_TOKEN") = 2;

  // Reference: https://taku910.github.io/mecab/doxygen/classMeCab_1_1Lattice.html
  py::class_<MeCab::Lattice>(m, "Lattice")
      .def(py::init([]() { return std::unique_ptr<MeCab::Lattice>(MeCab::Lattice::create()); }))
      .def("clear", &MeCab::Lattice::clear)
      .def("is_available", &MeCab::Lattice::is_available)
      .def("bos_node", &MeCab::Lattice::bos_node, py::return_value_policy::reference)
      .def("eos_node", &MeCab::Lattice::eos_node, py::return_value_policy::reference)
      .def("begin_nodes", py::overload_cast<size_t>(&MeCab::Lattice::begin_nodes, py::const_),
           py::return_value_policy::reference)
      .def("end_nodes", py::overload_cast<size_t>(&MeCab::Lattice::end_nodes, py::const_),
           py::return_value_policy::reference)
      .def("sentence", &MeCab::Lattice::sentence)
      .def("set_sentence", py::overload_cast<const char *>(&MeCab::Lattice::set_sentence))
      .def("set_sentence", py::overload_cast<const char *, size_t>(&MeCab::Lattice::set_sentence))
      .def("size", &MeCab::Lattice::size)
      .def("set_Z", &MeCab::Lattice::set_Z)
      .def("Z", &MeCab::Lattice::Z)
      .def("set_theta", &MeCab::Lattice::set_theta)
      .def("theta", &MeCab::Lattice::theta)
      .def("next", &MeCab::Lattice::next)
      .def("request_type", &MeCab::Lattice::request_type)
      .def("has_request_type", &MeCab::Lattice::has_request_type)
      .def("set_request_type", &MeCab::Lattice::set_request_type)
      .def("add_request_type", &MeCab::Lattice::add_request_type)
      .def("remove_request_type", &MeCab::Lattice::remove_request_type)
      .def("new_node", &MeCab::Lattice::newNode, py::return_value_policy::reference)
      .def("to_string", py::overload_cast<>(&MeCab::Lattice::toString), py::return_value_policy::copy)
      .def("to_string", py::overload_cast<const MeCab::Node *>(&MeCab::Lattice::toString),
           py::return_value_policy::copy)
      .def("to_string", py::overload_cast<char *, size_t>(&MeCab::Lattice::toString))
      .def("to_string", py::overload_cast<const MeCab::Node *, char *, size_t>(&MeCab::Lattice::toString))
      .def("enum_nbest_as_string", py::overload_cast<size_t>(&MeCab::Lattice::enumNBestAsString),
           py::return_value_policy::copy)
      .def("enum_nbest_as_string", py::overload_cast<size_t, char *, size_t>(&MeCab::Lattice::enumNBestAsString))
      .def("has_constraint", &MeCab::Lattice::has_constraint)
      .def("boundary_constraint", &MeCab::Lattice::boundary_constraint)
      .def("feature_constraint", &MeCab::Lattice::feature_constraint)
      .def("set_boundary_constraint", &MeCab::Lattice::set_boundary_constraint)
      .def("set_feature_constraint", &MeCab::Lattice::set_feature_constraint)
      .def("set_result", &MeCab::Lattice::set_result)
      .def("what", &MeCab::Lattice::what, py::return_value_policy::copy)
      .def("set_what", &MeCab::Lattice::set_what)
      .def("__len__", &MeCab::Lattice::size)
      .def(
          "__iter__",
          [](const MeCab::Lattice &self) {
            Iterator begin = Iterator(self.bos_node()->next);
            Iterator end = Iterator(self.eos_node());
            return py::make_iterator(begin, end);
          },
          py::keep_alive<0, 1>()) // 0 -> iterator, 1 -> self
      .def("__repr__", [](const MeCab::Lattice &self) {
        std::stringstream stream;
        stream << "Lattice(";
        stream << "text=\"" << escape(self.sentence()) << "\"";
        stream << ")";
        return stream.str();
      });
}