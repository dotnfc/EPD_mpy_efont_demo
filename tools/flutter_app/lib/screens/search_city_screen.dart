// SPDX-License-Identifier: MIT License
//
// screen/page to search for a city
// 

import 'package:eforecast/utils/cubit/search_cubit.dart';
import 'package:flutter/material.dart';
import 'package:search_autocomplete/search_autocomplete.dart';


class SearchCityScreen extends StatefulWidget {
  final String currentText;

  const SearchCityScreen({
    super.key,
    required this.currentText
  });

  @override
  State<SearchCityScreen> createState() => _SearchCityScreenState();
}

class _SearchCityScreenState extends State<SearchCityScreen> {
  final _cubit = SearchCubit();

  @override
  void initState() {
    super.initState();
    _cubit.init(widget.currentText);
  }

  @override
  Widget build(BuildContext context) {
    return 
      Scaffold(
        appBar: AppBar(
          title: const Text('查找城市编码'),
          backgroundColor: Colors.lightBlue,
          foregroundColor: Colors.white,
        ),
        body: StreamBuilder<SearchState>(
            stream: _cubit.stream,
            builder: (context, snapshot) {
              final state = snapshot.data ?? _cubit.state;
              
              return _buildContent(state);
            }),
        floatingActionButton: FloatingActionButton(
          onPressed: () {
            Navigator.pop(context, _cubit.state.current);
            debugPrint("${_cubit.state.current}");
          },
          backgroundColor: Colors.lightBlue,
          foregroundColor: Colors.white,
          child: Text('确认')
        ),
    );
  }

  Widget _buildContent(SearchState state) {
    return ListView(
      children: [
        const SizedBox(height: 10),
        _buildDefaultField(state),
      ],
    );
  }

  Widget _buildDefaultField(SearchState state) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: SearchAutocomplete<String>(
        options: state.listFiltered,
        initValue: state.current,
        onSearch: _cubit.search,
        onSelected: _cubit.select,
        getString: (value) => value,
        hintText: '待查询的城市...',
      ),
    );
  }
}
