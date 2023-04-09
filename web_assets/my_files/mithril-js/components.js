import { inject_select_file } from './components/select_file';

export default [
    {
        selector: 'button[data-provide-select_file]',
        component: inject_select_file,
    },
]
