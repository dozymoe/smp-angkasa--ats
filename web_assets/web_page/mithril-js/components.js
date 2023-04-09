import { inject_select_page } from './components/select_page';

export default [
    {
        selector: 'button[data-provide-select_page]',
        component: inject_select_page,
    },
]
