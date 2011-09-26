/* array_ptr
 *
 * a simple c style array ptr/size wrapper template for c++
 * with stl container functionality
 * and support for std::vector and boost::array
 *
 * Copyright (C) 2011 Stefan Zimmermann <zimmermann.code@googlemail.com>
 *
 * array_ptr is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * array_ptr is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with array_ptr.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef __ARRAY_PTR_HPP
#define __ARRAY_PTR_HPP

#include <cstdlib>

namespace array_ptr
{
  template<typename T>
  class array_ptr
  {
  private:
    T *values;
    std::size_t _size;

  public:
    typedef T value_type;

    typedef T* iterator;
    typedef const T* const_iterator;

    inline array_ptr(T *values = NULL, std::size_t size = 0) :
      values(values),
      _size(size)
    {}

    inline array_ptr(std::vector<T> &values) :
      values(&values[0]),
      _size(values.size())
    {}

    template<std::size_t SIZE>
    inline array_ptr(boost::array<T, SIZE> &values) :
      values(values.c_array()),
      _size(SIZE)
    {}

    inline array_ptr(const boost::tuple<T*, size_t> &values_and_size) :
      values(values_and_size.template get<0>()),
      _size(values_and_size.template get<1>())
    {}

    inline void reset(const array_ptr<T> &values)
    {
      *this = values;
    }

    inline void reset(T *values = NULL, std::size_t size = 0)
    {
      this->values = values;
      this->_size = size;
    }

    inline void reset(std::vector<T> &values)
    {
      this->values = &values[0];
      this->_size = values.size();
    }

    template<std::size_t SIZE>
    inline void reset(boost::array<T, SIZE> &values)
    {
      this->values = values.c_array();
      this->_size = SIZE;
    }

    inline void reset(const boost::tuple<T, size_t> &values_and_size)
    {
      this->values = values_and_size.template get<0>();
      this->_size = values_and_size.template get<1>();
    }

    inline T* get()
    {
      return this->values;
    }

    inline const T* get() const
    {
      return this->values;
    }

    inline operator T*()
    {
      return this->values;
    }

    inline operator const T*() const
    {
      return this->values;
    }

    inline T& operator[](std::size_t index)
    {
      return this->values[index];
    }

    inline const T& operator[](std::size_t index) const
    {
      return this->values[index];
    }

    inline std::size_t size() const
    {
      return this->_size;
    }

    inline iterator begin()
    {
      return iterator(this->values);
    }

    inline iterator end()
    {
      return iterator(this->values + this->_size);
    }

    inline const_iterator cbegin()
    {
      return const_iterator(this->values);
    }

    inline const_iterator cend()
    {
      return const_iterator(this->values + this->_size);
    }
  };
}

#include "const_array_ptr.hpp"

#endif
