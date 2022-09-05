import '../extensions';

class Stack {
  constructor() {
    this.items = []
  }

  push(element) {
    this.items.push(element);
  }

  pop() {
    if (this.isEmpty())
      throw "Stack Underflow"

    return this.items.pop();
  }

  peek() {
    return this.items.last();
  }

  size() {
    return this.items.length;
  }

  isEmpty() {
    return this.size() == 0;
  }
}

export default Stack;
