

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=0;
    if (typeof(v) == 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  var newcatalog = {
    " items": " baris",
    " of ": " dari ",
    " pages": " halaman",
    "Backward button": "Tombol mundur",
    "Clear search input": "Bersihkan pencarian",
    "Description": "Deskripsi",
    "File Select": "Pilih Berkas",
    "Forward button": "Tombol maju",
    "Image": "Gambar",
    "Images": "Gambar-Gambar",
    "Items per page": "Baris per halaman",
    "Overflow": "Luapan",
    "Preview": "Penampakan",
    "Search": "Pencarian",
    "Select": "Pilih",
    "Show modal": "Buka dialog",
    "Table Action Bar": "Bagian Aksi Tabel",
    "close modal": "tutup dialog",
    "items selected": "baris dipilih",
    "of ": "dari ",
    "select number of items per page": "pilih jumlah baris per halaman",
    "select page number to view": "pilihan halaman untuk ditampilkan"
  };
  for (var key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      var value = django.catalog[msgid];
      if (typeof(value) == 'undefined') {
        return msgid;
      } else {
        return (typeof(value) == 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      var value = django.catalog[singular];
      if (typeof(value) == 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value.constructor === Array ? value[django.pluralidx(count)] : value;
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      var value = django.gettext(context + '\x04' + msgid);
      if (value.indexOf('\x04') != -1) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      var value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.indexOf('\x04') != -1) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "j N Y, G.i",
    "DATETIME_INPUT_FORMATS": [
      "%d-%m-%Y %H.%M.%S",
      "%d-%m-%Y %H.%M.%S.%f",
      "%d-%m-%Y %H.%M",
      "%d-%m-%y %H.%M.%S",
      "%d-%m-%y %H.%M.%S.%f",
      "%d-%m-%y %H.%M",
      "%m/%d/%y %H.%M.%S",
      "%m/%d/%y %H.%M.%S.%f",
      "%m/%d/%y %H.%M",
      "%m/%d/%Y %H.%M.%S",
      "%m/%d/%Y %H.%M.%S.%f",
      "%m/%d/%Y %H.%M",
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M:%S.%f",
      "%Y-%m-%d %H:%M",
      "%Y-%m-%d"
    ],
    "DATE_FORMAT": "j N Y",
    "DATE_INPUT_FORMATS": [
      "%d-%m-%Y",
      "%d/%m/%Y",
      "%d-%m-%y",
      "%d/%m/%y",
      "%d %b %Y",
      "%d %B %Y",
      "%m/%d/%y",
      "%m/%d/%Y",
      "%Y-%m-%d"
    ],
    "DECIMAL_SEPARATOR": ",",
    "FIRST_DAY_OF_WEEK": 1,
    "MONTH_DAY_FORMAT": "j F",
    "NUMBER_GROUPING": 3,
    "SHORT_DATETIME_FORMAT": "d-m-Y G.i",
    "SHORT_DATE_FORMAT": "d-m-Y",
    "THOUSAND_SEPARATOR": ".",
    "TIME_FORMAT": "G.i",
    "TIME_INPUT_FORMATS": [
      "%H.%M.%S",
      "%H.%M",
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M"
    ],
    "YEAR_MONTH_FORMAT": "F Y"
  };

    django.get_format = function(format_type) {
      var value = django.formats[format_type];
      if (typeof(value) == 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }

}(this));

