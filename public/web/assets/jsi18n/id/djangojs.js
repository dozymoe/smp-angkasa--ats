

'use strict';
{
  const globals = this;
  const django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    const v = 0;
    if (typeof v === 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  const newcatalog = {
    "Backward button": "Tombol mundur",
    "Choose an option": "Pilih satu",
    "Clear all": "Hapus bersih",
    "Clear all selected items": "Batalkan pilihan",
    "Clear filter": "Hapus filter",
    "Clear search input": "Tampilkan semua",
    "Clear selection": "Bersihkan pencarian",
    "Close menu": "Tutup menu",
    "Close the side navigation menu": "Tutup navigasi samping",
    "Copied!": "Tersalin!",
    "Copy code": "Salin kode",
    "Data loaded.": "Data sudah siap.",
    "Description": "Deskripsi",
    "Drag and drop files here or upload": "Tarik berkas-berkas ke sini atau unggah",
    "File Select": "Pilih Berkas",
    "Forward button": "Tombol maju",
    "Image": "Gambar",
    "Images": "Gambar-Gambar",
    "Items per page": "Baris per halaman",
    "List of options": "Daftar pilihan",
    "Loading": "Persiapan",
    "Loading data failed.": "Gagal mengambil data.",
    "Loading data...": "Menyiapkan data...",
    "Multi select options": "Pilihan berganda",
    "Next page": "Halaman berikutnya",
    "Off": "Mati",
    "Open menu": "Buka dialog",
    "Overflow": "Luapan",
    "Page Select": "Pilih Laman",
    "Pages": "Laman-Laman",
    "Preview": "Penampakan",
    "Previous page": "Halaman sebelumnya",
    "Remove uploaded file": "Hapus berkas unggahan",
    "Search": "Pencarian",
    "Select": "Pilih",
    "Select AM/PM": "Pilih sebelum/sesudah siang",
    "Select time zone": "Pilih zona waktu",
    "Show less": "Kurangi tampilan",
    "Show modal": "Tutup dialog",
    "Show more": "Tampilkan lebih",
    "Show more icon": "Tampilkan tambahan icon",
    "Show password": "Tampilkan kata kunci",
    "Side navigation": "Navigasi samping",
    "Skip to main content": "Loncat ke konten",
    "Summary": "Ringkasan",
    "Switcher": "Penampil",
    "Table Action Bar": "Bagian Aksi Table",
    "Title": "Judul",
    "Toggle the expansion state of the navigation": "Buka tutup navigasi",
    "Toolbar Search": "Pencarian",
    "breadcrumb": "remahan",
    "close": "tutup",
    "close modal": "tutup dialog",
    "decrease number input": "kurangi",
    "increase number input": "tambah",
    "items selected": "baris terpilih",
    "of {total} pages": "dari {total} halaman",
    "on": "menyala",
    "page": "halaman",
    "select number of items per page": "pilih jumlah baris per halaman",
    "select page number to view": "pilih halaman yang akan ditampilkan",
    "tile": "ubin"
  };
  for (const key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      const value = django.catalog[msgid];
      if (typeof value === 'undefined') {
        return msgid;
      } else {
        return (typeof value === 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      const value = django.catalog[singular];
      if (typeof value === 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value.constructor === Array ? value[django.pluralidx(count)] : value;
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      let value = django.gettext(context + '\x04' + msgid);
      if (value.includes('\x04')) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      let value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.includes('\x04')) {
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
      const value = django.formats[format_type];
      if (typeof value === 'undefined') {
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
};

