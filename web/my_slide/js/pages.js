import { CreatePage } from './views/create';

export default [
    {
        path: '/slides/add',
        component: CreatePage,
    },
    {
        path: '/slides/:pk(\\d+)/edit',
        component: CreatePage,
    },
]
