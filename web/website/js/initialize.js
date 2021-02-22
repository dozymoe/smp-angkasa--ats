import { MDCBanner } from '@material/banner';
import { MDCCheckbox } from '@material/checkbox';
import { MDCDataTable } from '@material/data-table';
import { MDCDrawer } from '@material/drawer';
import { MDCFormField } from '@material/form-field';
import { MDCIconButtonToggle } from '@material/icon-button';
import { MDCList } from '@material/list';
import { MDCMenu } from '@material/menu';
import { MDCRipple } from '@material/ripple';
import { MDCSelect } from '@material/select';
import { MDCSnackbar } from '@material/snackbar';
import { MDCTextField } from '@material/textfield';
import { MDCTopAppBar } from '@material/top-app-bar';

let banners = [];
let snackbars = [];


export default function(app)
{
    app.topbar = MDCTopAppBar.attachTo(document.querySelector(
            '.mdc-top-app-bar'));
    app.topbar.setScrollTarget(document.getElementById('page-wrapper'));

    for (let el of document.querySelectorAll('.mdc-banner'))
    {
        banners.push(new MDCBanner(el));
    }
    _open_banner();

    for (let el of document.querySelectorAll('.mdc-data-table'))
    {
        new MDCDataTable(el);
    }
    for (let el of document.querySelectorAll('.mdc-button'))
    {
        new MDCRipple(el);
    }
    for (let el of document.querySelectorAll('.mdc-checkbox'))
    {
        const checkbox = new MDCCheckbox(el);
        const ff = el.closest('.mdc-form-field');
        if (ff)
        {
            let formField = new MDCFormField(ff);
            formField.input = checkbox;
        }
    }
    for (let el of document.querySelectorAll('.mdc-drawer'))
    {
        app.drawer = MDCDrawer.attachTo(el);
    }
    for (let el of document.querySelectorAll('.mdc-icon-button.toggle'))
    {
        new MDCIconButtonToggle(el);
    }
    for (let el of document.querySelectorAll('.mdc-list'))
    {
        new MDCList(el);
    }
    for (let el of document.querySelectorAll('.mdc-menu'))
    {
        new MDCMenu(el);
    }
    for (let el of document.querySelectorAll('.mdc-select'))
    {
        new MDCSelect(el);
    }
    for (let el of document.querySelectorAll('.mdc-snackbar'))
    {
        snackbars.push(new MDCSnackbar(el));
    }
    _open_snackbar();

    for (let el of document.querySelectorAll('.mdc-text-field'))
    {
        new MDCTextField(el);
    }

    if (document.body.classList.contains('has-drawer'))
    {
        app.topbar.listen('MDCTopAppBar:nav', () =>
                {
                    app.drawer.open = !app.drawer.open;
                });

        app.drawer.listen('MDCDrawer:closed', () =>
                {
                    let el = document.getElementById('page-wrapper')
                            .querySelector('[tabindex="0"]');
                    if (el) el.focus();
                });
    }
}


function _open_banner()
{
    let banner = banners.shift();
    if (!banner) return;
    banner.listen('MDCBanner:closed', _open_banner);
    banner.open();
}


function _open_snackbar()
{
    let snackbar = snackbars.shift();
    if (!snackbar) return;
    snackbar.listen('MDCSnackbar:closed', _open_snackbar);
    snackbar.open();
}
