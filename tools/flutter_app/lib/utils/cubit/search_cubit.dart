import 'package:flutter/material.dart';

import '../../data/city_map.dart';
import 'cubit_imitator.dart';

part 'search_state.dart';

class SearchCubit extends CubitImitator<SearchState> {
  SearchCubit() : super(const SearchState());

  void init(String currentText) {
    const list = CityMap.collocations;
    emit(state.copyWith(
      list: list,
      listFiltered: list,
      current: currentText
    ));
  }

  void select(String value) {
    emit(state.copyWith(current: value));
  }

  void search(String value) {
    final listFiltered = state.list.where((text) {
      // return text.toLowerCase().startsWith(value.toLowerCase());
      return text.toLowerCase().contains(value.toLowerCase());
    });

    emit(state.copyWith(listFiltered: [...listFiltered]));
  }
}
