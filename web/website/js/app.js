import CarbonDesignInit from './initialize-carbondesign';
import WebsiteInit from './initialize';
//-
import MyFile from './modules/my_files/components';
import Website from './modules/website/components';
//-
import SlidePages from '../../my_slide/js/pages';


const initializations = [
    CarbonDesignInit,
    WebsiteInit,
];


const components = [
    //...MyFile,
    ...Website,
];


const pages = [
    ...SlidePages,
];


import { ApplicationStorage } from '../../misc/jsfw/core/application';
import { initialize_app, run } from '../../misc/jsfw/core/bootstrap';

function onload()
{
    let app = new ApplicationStorage();
    initialize_app(app, {name: "SMP Angkasa ATS"}, initializations);
    run(app, components, pages, document.getElementById('js_app'));
}
if (document.readyState !== 'loading') onload();
else document.addEventListener('DOMContentLoaded', onload);
