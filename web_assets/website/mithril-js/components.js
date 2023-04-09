import { inject_rest_preview } from './components/rest_preview';


export default [
    {
        selector: 'button[data-provide-rest-preview]',
        component: inject_rest_preview,
    },
];
