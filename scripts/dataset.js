/* Numa Koudsie · dataset
   The named home of a simulation's numbers, in the convention of NetCDF, HDF5 and xarray: dimensions,
   coordinates, data variables and attributes. The simulation writes into it at the moment it computes a
   value (the typed arrays it draws from live inside it); the data panel, the walkthrough's live numbers and
   the Save button only read it. Nothing is recomputed on the way to the table.

   var ds = Sim.dataset({ title: 'Wave interference', attrs: { figure: 1 } });
   ds.dim('i', 350);                                   a dimension and its length
   ds.var('C', ['j', 'i'], Float32Array, { ... });     an array over dimensions; attrs describe it
   var C = ds.alloc('C');                              the array itself, sized to the dims; write into it
   ds.touch('C');                                      say that it changed (versions drive repaints)
   ds.var('lambda', [], 'float', { units: 'px' });     a scalar
   ds.set('lambda', 30);  ds.get('lambda');
   ds.npz()                                            a Blob: NumPy .npy files in a zip, plus dataset.json */
(function () {
    'use strict';
    var Sim = window.Sim || (window.Sim = {});

    var DTYPES = [
        [Float32Array, 'float32', '<f4'], [Float64Array, 'float64', '<f8'],
        [Int32Array, 'int32', '<i4'], [Int16Array, 'int16', '<i2'], [Int8Array, 'int8', '|i1'],
        [Uint32Array, 'uint32', '<u4'], [Uint16Array, 'uint16', '<u2'],
        [Uint8Array, 'uint8', '|u1'], [Uint8ClampedArray, 'uint8', '|u1']
    ];
    function dtypeOf(ctorOrArray) {
        for (var k = 0; k < DTYPES.length; k++) {
            if (ctorOrArray === DTYPES[k][0] || ctorOrArray instanceof DTYPES[k][0]) return DTYPES[k];
        }
        return null;
    }

    function Dataset(meta) {
        meta = meta || {};
        this.title = meta.title || 'dataset';
        this.attrs = meta.attrs || {};
        this.dims = {};
        this.vars = {};
        this.order = [];
    }
    Dataset.prototype.dim = function (name, size) {
        this.dims[name] = size;
        return size;
    };
    /* type: a typed-array constructor for arrays; 'float', 'int', 'bool' or 'str' for scalars */
    Dataset.prototype.var = function (name, dims, type, attrs) {
        var v = this.vars[name];
        if (!v) {
            v = this.vars[name] = { name: name, dims: dims.slice(), type: type, attrs: attrs || {}, data: undefined, version: 0 };
            this.order.push(name);
        } else {
            v.dims = dims.slice();
            v.type = type;
            if (attrs) v.attrs = attrs;
        }
        if (dims.length) this.alloc(name);
        return v;
    };
    Dataset.prototype.coord = function (name, dim, type, attrs) {
        attrs = attrs || {};
        attrs.coordinate = true;
        return this.var(name, [dim], type, attrs);
    };
    /* the array for an N-dimensional variable, (re)allocated to the current dimension sizes */
    Dataset.prototype.alloc = function (name) {
        var v = this.vars[name], n = 1, d;
        for (d = 0; d < v.dims.length; d++) n *= this.dims[v.dims[d]] || 0;
        if (!v.data || v.data.length !== n) v.data = new v.type(n);
        v.version++;
        return v.data;
    };
    Dataset.prototype.set = function (name, value) {
        var v = this.vars[name];
        if (v.data !== value) { v.data = value; v.version++; }
        return value;
    };
    Dataset.prototype.get = function (name) {
        var v = this.vars[name];
        return v ? v.data : undefined;
    };
    Dataset.prototype.touch = function (name) { this.vars[name].version++; };
    Dataset.prototype.has = function (name) { return !!this.vars[name]; };
    Dataset.prototype.shape = function (name) {
        var ds = this;
        return this.vars[name].dims.map(function (d) { return ds.dims[d] || 0; });
    };
    Dataset.prototype.size = function (name) {
        return this.shape(name).reduce(function (a, b) { return a * b; }, 1);
    };
    /* row-major flat index of a 2-D element */
    Dataset.prototype.index = function (name, j, i) { return j * (this.dims[this.vars[name].dims[1]] || 0) + i; };
    Dataset.prototype.at = function (name, idx) {
        var v = this.vars[name];
        return v.dims.length ? v.data[idx] : v.data;
    };
    Dataset.prototype.dtype = function (name) {
        var v = this.vars[name];
        if (!v.dims.length) return v.type;
        var dt = dtypeOf(v.type);
        return dt ? dt[1] : 'array';
    };
    /* every variable that lies along one dimension, coordinates first */
    Dataset.prototype.along = function (dim) {
        var ds = this, out = [];
        this.order.forEach(function (n) {
            var v = ds.vars[n];
            if (v.dims.length === 1 && v.dims[0] === dim) out.push(n);
        });
        out.sort(function (a, b) { return (ds.vars[b].attrs.coordinate ? 1 : 0) - (ds.vars[a].attrs.coordinate ? 1 : 0); });
        return out;
    };

    /* ---------- export: NumPy .npy inside a stored zip, with dataset.json ---------- */
    var enc = function (s) { return new TextEncoder().encode(s); };
    function npy(arr, shape) {
        var dt = dtypeOf(arr);
        var header = "{'descr': '" + dt[2] + "', 'fortran_order': False, 'shape': (" + shape.join(', ') + (shape.length === 1 ? ',' : '') + "), }";
        var pad = (64 - ((10 + header.length + 1) % 64)) % 64, i;
        for (i = 0; i < pad; i++) header += ' ';
        header += '\n';
        var hb = enc(header), out = new Uint8Array(10 + hb.length + arr.byteLength);
        out.set([0x93, 0x4e, 0x55, 0x4d, 0x50, 0x59, 1, 0], 0);
        out[8] = hb.length & 255;
        out[9] = hb.length >> 8;
        out.set(hb, 10);
        out.set(new Uint8Array(arr.buffer, arr.byteOffset, arr.byteLength), 10 + hb.length);
        return out;
    }
    var CRC = (function () {
        var t = new Uint32Array(256), n, k, c;
        for (n = 0; n < 256; n++) {
            c = n;
            for (k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
            t[n] = c >>> 0;
        }
        return t;
    })();
    function crc32(bytes) {
        var c = 0xffffffff;
        for (var i = 0; i < bytes.length; i++) c = CRC[(c ^ bytes[i]) & 255] ^ (c >>> 8);
        return (c ^ 0xffffffff) >>> 0;
    }
    /* a zip with no compression: every tool opens it, and NumPy reads it as an .npz */
    function zip(entries) {
        var parts = [], central = [], offset = 0, i;
        function u16(v) { return [v & 255, (v >> 8) & 255]; }
        function u32(v) { return [v & 255, (v >> 8) & 255, (v >> 16) & 255, (v >>> 24) & 255]; }
        var now = new Date(), dosTime = (now.getHours() << 11) | (now.getMinutes() << 5) | (now.getSeconds() >> 1);
        var dosDate = ((now.getFullYear() - 1980) << 9) | ((now.getMonth() + 1) << 5) | now.getDate();
        for (i = 0; i < entries.length; i++) {
            var name = enc(entries[i].name), data = entries[i].bytes, crc = crc32(data);
            var local = new Uint8Array([].concat([0x50, 0x4b, 3, 4], u16(20), u16(0x0800), u16(0), u16(dosTime), u16(dosDate), u32(crc), u32(data.length), u32(data.length), u16(name.length), u16(0)));
            parts.push(local, name, data);
            central.push(new Uint8Array([].concat([0x50, 0x4b, 1, 2], u16(20), u16(20), u16(0x0800), u16(0), u16(dosTime), u16(dosDate), u32(crc), u32(data.length), u32(data.length), u16(name.length), u16(0), u16(0), u16(0), u16(0), u32(0), u32(offset))), name);
            offset += local.length + name.length + data.length;
        }
        var cdSize = 0;
        for (i = 0; i < central.length; i++) cdSize += central[i].length;
        var end = new Uint8Array([].concat([0x50, 0x4b, 5, 6], u16(0), u16(0), u16(entries.length), u16(entries.length), u32(cdSize), u32(offset), u16(0)));
        return new Blob(parts.concat(central, [end]), { type: 'application/zip' });
    }
    Dataset.prototype.npz = function (extra) {
        var ds = this, entries = [], meta = { title: this.title, attrs: this.attrs, dims: this.dims, coords: [], data_vars: {} };
        this.order.forEach(function (n) {
            var v = ds.vars[n], rec = { dims: v.dims, attrs: v.attrs };
            if (v.dims.length) {
                var file = n + '.npy';
                rec.dtype = ds.dtype(n);
                rec.shape = ds.shape(n);
                rec.file = file;
                entries.push({ name: file, bytes: npy(v.data, rec.shape) });
            } else {
                rec.dtype = v.type;
                rec.value = v.data === undefined ? null : v.data;
            }
            if (v.attrs.coordinate) meta.coords.push(n);
            meta.data_vars[n] = rec;
        });
        entries.push({ name: 'dataset.json', bytes: enc(JSON.stringify(meta, null, 2)) });
        (extra || []).forEach(function (e) { entries.push({ name: e.name, bytes: typeof e.bytes === 'string' ? enc(e.bytes) : e.bytes }); });
        return zip(entries);
    };

    Sim.dataset = function (meta) { return new Dataset(meta); };
    Sim.Dataset = Dataset;
})();
