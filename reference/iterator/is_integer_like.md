# is-integer-like
* iterator[meta header]
* std[meta namespace]
* variable[meta id-type]
* cpp20[meta cpp]

```cpp
namespace std {
  template<class T>
  inline constexpr bool is-integer-like = /*see below*/;

  template<class T>
  inline constexpr bool is-signed-integer-like = /*see below*/;
}
```

## 概要

これらの説明専用の変数テンプレートは、任意の型`T`が符号付/なし整数型そのものあるいはそれと同様に扱える型である場合に`true`を示すものである。

これは標準ライブラリ内において、イテレータの差分型（`difference_type`）として実装定義の整数型の使用を許可するためにコンセプトの文脈で使用される。

## 効果

`is-integer-like<T>`は`T`が[`integral`](/reference/concepts/integral.md)のモデルとなるか*integer-class*である時に`true`を示す。  
`is-signed-integer-like<T>`は`T`が[`signed_integral`](/reference/concepts/signed_integral.md)のモデルとなるか*signed-integer-class*である時に`true`を示す。

## (signed-)integer-class型

*integer-class*型は組み込みの整数型と同じように動作する実装定義のクラス型である。

*integer-class*型の表現可能な範囲はそれが定義する値の連続集合であり、`0`と`1`を必ず含んでいなければならない。この時、その範囲に負の数が含まれていればその型は*signed-integer-class*型であり、それ以外のものは*unsigned-integer-class*型である。

### 要件

`I`をある*integer-class*型、`B`を少なくとも`I`と同じ範囲の値を表現可能で同じ幅を持つ別の*integer-class*型とする。  
`I`の値`a, b`、`a, b`それぞれと同じ値を表現する`B`の値`x, y`と任意の整数型の値`c`について次のことが成り立つ。

- 式`@x`が適格である全ての単項演算子`@`について`@a`もまた適格であり、共に同じ値、効果、値カテゴリを持つ。`@x`が`bool`型を示す場合`@a`もまた`bool`型を示すが。`@x`が`B`を示す場合は`@a`は`I`を示す。
- 式`c @= x`が適格である全ての（複合）代入演算子`@=`について`c @= a`もまた適格であり、共に同じ値、効果を持つ。式`c @= a`の結果は`c`を参照する*lvalue*となる。
- 式`x @ y`が適格である全ての二項演算子`@`について`a @ b`もまた適格であり、結果の値を`I`が表現できる場合は共に同じ値、効果、値カテゴリを持つ。`x @ y`が`bool`型を示す場合`a @ b`もまた`bool`型を示すが。`x @ y`が`B`を示す場合は`a @ b`は`I`を示す。
- *integer-class*型の値は任意の整数型に明示的に変換でき、任意の整数型の値は*integer-class*型に暗黙的にも明示的にも変換できる。それらの変換は例外を送出しない。
- *integer-class*型の式`E`は`bool(E != I(0))`のように文脈的に`bool`に変換できる。
- *integer-class*型は[`regular`](/reference/concepts/regular.md)及び[`totally_ordered`](/reference/concepts/totally_ordered.md)のモデルとなる。
- 値初期化された*integer-class*型の値は`0`になる。

*integer-class*型`I`について[`numeric_limits<I>`](/reference/limits/numeric_limits.md)の特殊化は次のような値を示す。

- `numeric_limits<I>::is_specialized == true`
- [`numeric_limits<I>::is_signed`](/reference/limits/numeric_limits/is_signed.md)` == true`
    - `I`が*signed-integer-class*型の場合のみ
- [`numeric_limits<I>::digits`](/reference/limits/numeric_limits/digits.md)は`I`の幅と等しい
- [`numeric_limits<I>::digits10`](/reference/limits/numeric_limits/digits10.md)は`static_cast<int>(digits * log10(2))`と等しい
- [`numeric_limits<I>::min()`](/reference/limits/numeric_limits/min.md)と[`numeric_limits<I>::max()`](/reference/limits/numeric_limits/max.md)はそれぞれ、`I`の表現可能な値の最小値と最大値を返す。[`numeric_limits<I>::lowest()`](/reference/limits/numeric_limits/lowest.md)は`numeric_limits<I>::max()`を返す。


## バージョン
### 言語
- C++20

## 関連項目

- [`weakly_incrementable`](weakly_incrementable.md)
- [`iota_view`](/reference/ranges/iota_view.md.nolink)

## 参照

- [P1522R1 Iterator Difference Type and Integer Overflow](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1522r1.pdf)