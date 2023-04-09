import CarbonDesignInit from './initialize-carbondesign';
import WebsiteInit from './initialize';
//-
import MyFile from './my_files/mithril-js/components';
import Website from './website/mithril-js/components';
import WebPage from './web_page/mithril-js/components';

const initializations = [
    CarbonDesignInit,
    WebsiteInit,
];


const components = [
    ...MyFile,
    ...WebPage,
    ...Website,
];


const pages = [
];


import { initialize_app, run } from './fw/core/bootstrap';
import { Application } from './application';

function onload()
{
    let app = new Application();
    initialize_app(app, {name: "SMP Angkasa ATS"}, initializations);
    run(app, components, pages, document.getElementById('js_app'));
}
if (document.readyState !== 'loading') onload();
else document.addEventListener('DOMContentLoaded', onload);
