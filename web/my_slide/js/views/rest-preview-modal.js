import CarbonModal from 'carbon-components/src/components/modal/modal';
import m from 'mithril/hyperscript';
import m_redraw from 'mithril/redraw';
import createStore from 'unistore';
import { mapActions } from 'unistore/src/util';
//--
import { msgbus } from '../../../misc/msgbus';
import { Slot } from '../../../misc/carbondesign-js/base';
import { Modal } from '../../../misc/carbondesign-js/modal';

const ATTRIBUTE_NAME = 'data-provide-rest-preview';


const StoreActions =
{
    setPreview(state, preview)
    {
        return {preview: preview}
    },
}


export class RestPreviewModal
{
    constructor(app)
    {
        this.app = app;
        this.txt_title = gettext("Preview");
    }

    oninit(vnode)
    {
        this.store = createStore({
            preview: '',
        });
        this.actions = mapActions(StoreActions, this.store);

        this.ontrigger_click = this.ontrigger_click.bind(this);
    }

    view(vnode)
    {
        let state = this.store.getState();

        return (
//##
m(Modal, null, [
  m(Slot,
    {name: 'heading'},
    this.txt_title),
  m.trust(state.preview),
  ])
//##
        )
    }

    oncreate(vnode)
    {
        this.component = CarbonModal.create(vnode.dom);

        for (let btn of document.querySelectorAll('button[' + ATTRIBUTE_NAME +
                ']'))
        {
            btn.addEventListener('click', this.ontrigger_click);
        }
    }

    onremove(vnode)
    {
        for (let btn of document.querySelectorAll('button[' + ATTRIBUTE_NAME +
                ']'))
        {
            btn.removeEventListener('click', this.ontrigger_click);
        }

        this.component.release();
    }

    async ontrigger_click(event)
    {
        let btn = event.target || event.currentTarget;
        let textarea = document.getElementById(btn.getAttribute(ATTRIBUTE_NAME));

        this.component.show();

        let formData = new FormData();
        formData.append('body', textarea.value);
        let resp = await msgbus('/api/render-html').body(formData).post();
        let html = await resp.text();
        this.actions.setPreview(html);
        m_redraw();
    }
}
