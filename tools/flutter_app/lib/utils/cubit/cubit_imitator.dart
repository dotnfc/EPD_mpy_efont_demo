import 'dart:async';

class CubitImitator<S> {
  late S state;

  CubitImitator(this.state);

  final _controller = StreamController<S>.broadcast();

  Stream<S> get stream => _controller.stream;

  void emit(S state) {
    this.state = state;

    _controller.add(this.state);
  }
}
