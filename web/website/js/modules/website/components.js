import { InjectWysiwyg } from './views.jsx';


export default [
    {
        selector: 'textarea[data-provide-editor="ace"]',
        component: InjectWysiwyg,
    },
];
