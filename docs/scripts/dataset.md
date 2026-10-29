# public/scripts/dataset.js

| | |
|---|---|
| File | [public/scripts/dataset.js](../../public/scripts/dataset.js), 175 lines, 8.6 kB (8 617 bytes) |
| Loaded by | the eleven simulation pages, third, right after `sim.js` and before the page's own script (line numbers in the load-order table of [sim.md](sim.md#load-order-on-the-pages)), the two pages of Iron, Cotton and the Head ([portfolios.md](../portfolios.md#the-data-panel-of-the-study)), the ideal and servo presses of the Hydraulic Press Study, and Droplet Collection, before its inline script ([portfolios.md](../portfolios.md#the-data-panel-the-bookkeeper-since-24-october-2026)). No other page loads it. |
| Defines | `Sim.dataset(meta)` on `window.Sim` ([dataset.js:174-175](../../public/scripts/dataset.js#L174-L175)); creates `window.Sim` if it does not exist yet ([dataset.js:17](../../public/scripts/dataset.js#L17)) |
| Used by | each page's script (writes), [datalog.js](datalog.md) (reads, saves), each page's `Sim.live()` (reads) |

`dataset.js` gives a simulation page one named store for all its numbers, built like a NetCDF file or an xarray `Dataset`:
named dimensions, typed-array variables laid out over those dimensions, scalars, and attributes that say what each
quantity is, in which units, and on which line it is computed. The page writes each number into the store at the line that
computes it, every frame, overwriting the previous frame. The data panel, the walkthrough's "Now" column and the Save button
only read it; nothing is recomputed for display ([dataset.js:1-5](../../public/scripts/dataset.js#L1-L5)). The file also
holds the writer that turns the store into a NumPy `.npz` archive.

## How it works

### The picture

Think of the page of a lab notebook that is wiped and rewritten every frame. The page has a ruled table for each array (a
row per point of the grid, a column per component), a line per single number, and a margin note beside each entry: its
symbol, its unit, the formula, where it was computed. At any instant the notebook holds exactly one frame, so it never grows.
Anyone may read the page; only the simulation writes on it.

### The model

| Concept | In the code | Example (Fig. 2, [Double Pendulum.html](../../public/simulations/Double%20Pendulum.html)) |
|---|---|---|
| Dataset | `new Dataset(meta)`: `title`, global `attrs`, `dims`, `vars`, `order` ([dataset.js:32-39](../../public/scripts/dataset.js#L32-L39)) | `Sim.dataset({ title: 'Double pendulum', attrs: { figure: 2, … } })` ([L406](../../public/simulations/Double%20Pendulum.html#L406)) |
| Dimension | a name and a length in `dims` ([dataset.js:40-43](../../public/scripts/dataset.js#L40-L43)) | `ds.dim('q', 4)` ([L414](../../public/simulations/Double%20Pendulum.html#L414)) |
| Array variable | `{ name, dims, type: <typed-array constructor>, attrs, data, version }` ([dataset.js:48](../../public/scripts/dataset.js#L48)) | `ds.var('y', ['q'], Float64Array, { … })` ([L415](../../public/simulations/Double%20Pendulum.html#L415)) |
| Scalar | a variable with `dims = []`; `type` is a string | `ds.set('th1', s[0])` ([L654](../../public/simulations/Double%20Pendulum.html#L654)) |
| Coordinate | a 1-D variable with `attrs.coordinate = true` ([dataset.js:58-62](../../public/scripts/dataset.js#L58-L62)) | `ds.coord('x', 'i', Float64Array, …)` ([Circular Wave Interference Visualization.html:547](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L547)) |
| Version | an integer per variable, raised on every change ([dataset.js:68](../../public/scripts/dataset.js#L68), [73](../../public/scripts/dataset.js#L73), [80](../../public/scripts/dataset.js#L80)) | `ds.touch('y')` after writing into the array in place ([L653](../../public/simulations/Double%20Pendulum.html#L653)) |

Arrays are stored flat in row-major order: element $(j, i)$ of a variable with dimensions $(J, I)$ sits at index
$jI + i$. The first dimension is the row.

### The mechanism, in the order a page uses it

1. **Create.** `Sim.dataset(meta)` returns a new `Dataset` ([dataset.js:174](../../public/scripts/dataset.js#L174)).
2. **Declare.** `ds.dim(name, size)` records a length. `ds.var(name, dims, type, attrs)` declares a variable once and keeps
   its declaration order in `order` ([dataset.js:45-57](../../public/scripts/dataset.js#L45-L57)). Declaring the same name
   again updates `dims`, `type` and (if given) `attrs` in place. For an array (`dims.length > 0`) it allocates the data at
   once ([dataset.js:55](../../public/scripts/dataset.js#L55)).
3. **Allocate.** `ds.alloc(name)` makes a typed array whose length is the product of the current dimension lengths, and
   returns it ([dataset.js:64-70](../../public/scripts/dataset.js#L64-L70)). It only replaces the array when the length has
   changed, so a page can hold on to the returned array between frames; after a resize (a new `dim` length) the page calls
   `alloc` again and takes the new array. Every call raises the version.
4. **Write.** For an array, the page writes into the array it got from `alloc` and calls `ds.touch(name)` to raise the
   version ([dataset.js:80](../../public/scripts/dataset.js#L80)). For a scalar, `ds.set(name, value)` stores the value and
   raises the version only if the value differs from the stored one ([dataset.js:71-75](../../public/scripts/dataset.js#L71-L75)).
   `set` can also replace a whole array by another array object.
5. **Read.** `ds.get(name)` returns the scalar or the array itself, not a copy ([dataset.js:76-79](../../public/scripts/dataset.js#L76-L79)).
   Readers that need one consistent instant copy it themselves (the data panel's table does, [datalog.js:652-657](../../public/scripts/datalog.js#L652-L657)).
6. **Describe.** `shape`, `dtype` and `along` answer the questions the panel asks: how big, which NumPy type, which
   variables share a dimension ([dataset.js:82-101](../../public/scripts/dataset.js#L82-L101)).
7. **Export.** `ds.npz(extra)` writes every array as a `.npy` file and every scalar into `dataset.json`, adds the `extra`
   files, and packs them into an uncompressed zip that NumPy opens as an `.npz` ([dataset.js:152-172](../../public/scripts/dataset.js#L152-L172)).
   The byte layout is explained in [datalog.md, "The .npz writer"](datalog.md#the-npz-writer-byte-by-byte).

The version numbers are how readers avoid work: the data panel recomputes min, max and mean of an array and redraws its
sparkline only when the version has moved ([datalog.js:316-322](../../public/scripts/datalog.js#L316-L322),
[datalog.js:393](../../public/scripts/datalog.js#L393)).

### Types

Array types and their NumPy names, from the table `DTYPES` ([dataset.js:19-24](../../public/scripts/dataset.js#L19-L24)):

| Constructor | `dtype()` | `.npy` `descr` |
|---|---|---|
| `Float32Array` | `float32` | `<f4` |
| `Float64Array` | `float64` | `<f8` |
| `Int32Array` | `int32` | `<i4` |
| `Int16Array` | `int16` | `<i2` |
| `Int8Array` | `int8` | `\|i1` |
| `Uint32Array` | `uint32` | `<u4` |
| `Uint16Array` | `uint16` | `<u2` |
| `Uint8Array` | `uint8` | `\|u1` |
| `Uint8ClampedArray` | `uint8` | `\|u1` |

`<` means little-endian; `|` means byte order does not apply (one byte). For a scalar, `dtype()` returns the type string the
page gave ([dataset.js:88](../../public/scripts/dataset.js#L88)). The comment names `'float'`, `'int'`, `'bool'`, `'str'` and `'uint8'`
([dataset.js:44](../../public/scripts/dataset.js#L44)); the pages include one `'uint8'` scalar holding an RGB
triple ([Circular Wave Interference Visualization.html:572](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L572)).
Across the ten pages of 14 October 2026 a grep found 546 `ds.var` calls (on 29 October 2026 the eleven pages hold 757:
`cat public/simulations/*.html | grep -o "ds\.var(" | wc -l`; the breakdown below and the attribute counts are those of 14 October): 137 arrays (127 `Float64Array`, 7 `Float32Array`, 2 `Int32Array`,
1 `Uint8ClampedArray`) and 409 scalars (311 `'float'`, 63 `'int'`, 28 `'bool'`, 6 `'str'`, 1 `'uint8'`), plus 13
`ds.coord` calls, all `Float64Array`.

### Attributes the rest of the site reads

`attrs` is a free object, but `datalog.js` gives these keys a meaning (counts, of 14 October 2026, are occurrences in the ten pages' `ds.var` and
`ds.coord` calls):

| Key | Used for | Count |
|---|---|---|
| `symbol` | HTML symbol shown in the panel ([datalog.js:116](../../public/scripts/datalog.js#L116)) | 559 |
| `long_name` | one-line meaning, the Meaning column of the ledger and the headline's tooltip ([datalog.js:257](../../public/scripts/datalog.js#L257)) | 559 |
| `computed_in` | function or line that computes it, shown in Check ([datalog.js:814](../../public/scripts/datalog.js#L814)) | 559 |
| `digits` | decimals shown, default 4 ([datalog.js:117](../../public/scripts/datalog.js#L117)) | 524 |
| `formula` | formula shown under the meaning in the ledger, in Check and above an open array ([datalog.js:256](../../public/scripts/datalog.js#L256), [datalog.js:816](../../public/scripts/datalog.js#L816)) | 372 |
| `units` | SI or pixel unit ([datalog.js:118](../../public/scripts/datalog.js#L118)) | 355 |
| `source` | Check text when there is no independent formula, through `T()` ([datalog.js:828](../../public/scripts/datalog.js#L828)) | 145 |
| `updates` | when it changes ([datalog.js:815](../../public/scripts/datalog.js#L815)) | 119 |
| `coordinate` | set by `coord`; coordinates are listed first by `along` and in `dataset.json` | set by 13 `ds.coord` calls |
| `colour` | `true`: the scalar is an RGB triple, shown as a swatch ([datalog.js:326](../../public/scripts/datalog.js#L326)) | 1 |
| `sci` | `true`: the value is shown in scientific notation, 2.1×10⁻⁹, not as a row of zeros: residuals and relative errors ([datalog.js:327](../../public/scripts/datalog.js#L327)) | 5 (Figs. 9 and 10: `bal_now`, `fres_now`, `ebal_now`, `balance` twice) |
| `cw` | column width of the array table ([datalog.js:686](../../public/scripts/datalog.js#L686)) | 2 |
| `drawn_note` | Check text when nothing is read back ([datalog.js:839](../../public/scripts/datalog.js#L839)) | 0 |

## Public interface

| Name | Lines | Arguments | What it does / returns |
|---|---|---|---|
| `Sim.dataset` | [174](../../public/scripts/dataset.js#L174) | `meta = { title, attrs }` | A new `Dataset`. |
| `ds.dim` | [40-43](../../public/scripts/dataset.js#L40-L43) | `name, size` | Sets the length; returns `size`. Does not reallocate existing arrays. |
| `ds.var` | [45-57](../../public/scripts/dataset.js#L45-L57) | `name, dims, type, attrs` | Declares or redeclares; allocates arrays; returns the variable record. |
| `ds.coord` | [58-62](../../public/scripts/dataset.js#L58-L62) | `name, dim, type, attrs` | `var(name, [dim], type, attrs)` with `attrs.coordinate = true`. |
| `ds.alloc` | [64-70](../../public/scripts/dataset.js#L64-L70) | `name` | The array, sized to the current dims; raises the version. |
| `ds.set` | [71-75](../../public/scripts/dataset.js#L71-L75) | `name, value` | Stores; raises the version if the value changed; returns `value`. Throws if `name` was never declared. |
| `ds.get` | [76-79](../../public/scripts/dataset.js#L76-L79) | `name` | The stored value or array, `undefined` for an unknown name. |
| `ds.touch` | [80](../../public/scripts/dataset.js#L80) | `name` | Raises the version after an in-place write. |
| `ds.has` | [81](../../public/scripts/dataset.js#L81) | `name` | Whether the variable exists. |
| `ds.shape` | [82-85](../../public/scripts/dataset.js#L82-L85) | `name` | Array of dimension lengths (`[]` for a scalar). |
| `ds.dtype` | [86-91](../../public/scripts/dataset.js#L86-L91) | `name` | NumPy type name of an array (`'array'` if unknown), or the scalar's type string. |
| `ds.along` | [93-101](../../public/scripts/dataset.js#L93-L101) | `dim` | Names of all 1-D variables over `dim`, coordinates first, otherwise in declaration order. |
| `ds.npz` | [152-172](../../public/scripts/dataset.js#L152-L172) | `extra = [{ name, bytes }]` (`bytes` a string or `Uint8Array`) | A `Blob` (`application/zip`): one `<name>.npy` per array, `dataset.json`, then the extra files. |

Fields read directly by `datalog.js`: `ds.title`, `ds.dims`, `ds.vars[name]` (its `dims`, `type`, `attrs`, `data`,
`version`) and `ds.order` ([datalog.js:114](../../public/scripts/datalog.js#L114), [datalog.js:1065](../../public/scripts/datalog.js#L1065)).

## Internal functions

| Name | Lines | What it does |
|---|---|---|
| `dtypeOf` | [25-30](../../public/scripts/dataset.js#L25-L30) | Finds the `DTYPES` row for a constructor or an array instance; `null` if none. |
| `Dataset` | [32-39](../../public/scripts/dataset.js#L32-L39) | Private constructor used by `Sim.dataset`. |
| `enc` | [104](../../public/scripts/dataset.js#L104) | UTF-8 encodes a string with `TextEncoder`. |
| `npy` | [105-118](../../public/scripts/dataset.js#L105-L118) | One NumPy `.npy` file (version 1.0) as bytes. |
| `CRC` (IIFE) | [119-127](../../public/scripts/dataset.js#L119-L127) | The 256-entry CRC-32 table, built once. |
| `crc32` | [128-132](../../public/scripts/dataset.js#L128-L132) | CRC-32 of a byte array. |
| `zip` | [134-151](../../public/scripts/dataset.js#L134-L151) | Packs `[{ name, bytes }]` into a stored (uncompressed) zip `Blob`. |
| `u16`, `u32` (in `zip`) | [136-137](../../public/scripts/dataset.js#L136-L137) | Little-endian 2- and 4-byte fields. |

## State it keeps

Only what each `Dataset` object holds: `title`, `attrs`, `dims`, `vars`, `order`. The module itself keeps the constant
`DTYPES` table and the `CRC` table. No storage, no DOM, no timers, no listeners.

## Timing and events

None. The file reacts to nothing; it runs only when a page or the data panel calls it. Its cost per frame is the cost of the
`set` and `touch` calls the page makes: one property write and one comparison each.

## Contracts with other files

- Must load after `sim.js`, which creates `window.Sim` afresh ([sim.js:415](../../public/scripts/sim.js#L415)); loaded
  before it, `Sim.dataset` would be wiped.
- Each page makes exactly one store and hands it to the panel as `Sim.data.ds` (for example
  [Double Pendulum.html:769](../../public/simulations/Double%20Pendulum.html#L769)). The `Sim.dataset(...)` call of each page:
  [Fig. 1 L526](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L526),
  [Fig. 2 L406](../../public/simulations/Double%20Pendulum.html#L406),
  [Fig. 3 L561](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L561),
  [Fig. 4 L747](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L747),
  [Fig. 5 L578](../../public/simulations/water-wave.html#L578),
  [Fig. 6 L507](../../public/simulations/wave-interference.html#L507),
  [Fig. 7 L710](../../public/simulations/phasor-sums.html#L710),
  [Fig. 8 L638](../../public/simulations/draw-decompose.html#L638),
  [Fig. 9 L615](../../public/simulations/driven-oscillator.html#L615),
  [Fig. 10 L566](../../public/simulations/wind-turbine.html#L566).
- `datalog.js` builds a second, temporary `Dataset` for a recorded round and saves it with the same `npz`
  ([datalog.js:1278-1286](../../public/scripts/datalog.js#L1278-L1286)).
- Each page's `Sim.live()` reads the store and formats strings for the walkthrough (for example
  [Double Pendulum.html:684-696](../../public/simulations/Double%20Pendulum.html#L684-L696)); see [walk.md](walk.md).
- Each page's own documentation lists its dimensions, variables and the line where each is written
  ([../simulations/](../simulations/)).

## How to change it safely

- An array's length must equal the product of its dimension lengths. `npy` writes the shape from the dimensions
  ([dataset.js:159](../../public/scripts/dataset.js#L159)) and the bytes from the array
  ([dataset.js:116](../../public/scripts/dataset.js#L116)); if they disagree, NumPy refuses the file. After changing a
  dimension with `dim`, call `alloc` for every variable over it.
- After writing into an array in place, call `touch`, or the panel's statistics and thumbnail stay on the old frame.
- Use only the typed arrays in `DTYPES` for arrays. Any other constructor (a plain `Array`, `BigInt64Array`) makes
  `dtypeOf` return `null`, and `npy` then throws on `dt[2]` ([dataset.js:107](../../public/scripts/dataset.js#L107)), which
  breaks Save for the whole store.
- If `set` replaces an array with one of a different typed-array type than declared, the `.npy` header follows the actual
  array ([dataset.js:106](../../public/scripts/dataset.js#L106)) but `dataset.json` reports the declared type
  ([dataset.js:158](../../public/scripts/dataset.js#L158)). Keep them the same.
- The writer assumes a little-endian machine: it copies the typed array's bytes as they are in memory
  ([dataset.js:116](../../public/scripts/dataset.js#L116)) and labels them `<`. Every common browser platform is
  little-endian; this is not checked.
- Test a change by saving from one page and loading the archive in Python (see [datalog.md](datalog.md#the-npz-writer-byte-by-byte)).

## Notes for maintainers

1. Fixed on 2026-10-15: unused index, at, size and the Dataset constructor export were removed; shape remains for NPZ export (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)).
2. Fixed on 2026-10-15: the scalar type comment includes uint8 (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).
3. The attribute `drawn_note`, read at [datalog.js:839](../../public/scripts/datalog.js#L839), is set by no page.
4. `ds.set` on an undeclared name throws a `TypeError` ([dataset.js:73](../../public/scripts/dataset.js#L73)) while
   `ds.get` returns `undefined`. Whether this difference is intended is not determined from the code.
