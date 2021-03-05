import { InjectReSTPreview } from './views.jsx';
import { InjectMenu } from './views.jsx';


export default [
    {
        selector: 'button[data-provide-rest-preview]',
        component: InjectReSTPreview,
    },
    {
        selector: '[data-provide-menu]',
        component: InjectMenu,
    },
];
