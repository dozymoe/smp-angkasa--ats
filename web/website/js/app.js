import { create_application, run
       } from '../../../lib/fireh_react/core/application.jsx';
//-
import WebsiteInit from './initialize.js';
//-
import MyFile from './modules/my_file/components.js';
import Website from './modules/website/components.js';


const initializations = [
    WebsiteInit,
];


const components = [
    ...MyFile,
    ...Website,
];


const pages = [
];


function onload()
{
    let app = create_application({name: "SMP Angkasa ATS"}, initializations);
    run(app, components, pages, document.getElementById('js_app'));
}
if (document.readyState !== 'loading') onload();
else document.addEventListener('DOMContentLoaded', onload);
