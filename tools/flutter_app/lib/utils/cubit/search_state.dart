part of 'search_cubit.dart';

@immutable
class SearchState {
  final List<String> list;
  final List<String> listFiltered;
  final String? current;

  const SearchState({
    this.list = const [],
    this.listFiltered = const [],
    this.current,
  });

  SearchState copyWith({
    List<String>? list,
    List<String>? listFiltered,
    String? current,
  }) {
    return SearchState(
      list: list ?? this.list,
      listFiltered: listFiltered ?? this.listFiltered,
      current: current ?? this.current,
    );
  }
}
