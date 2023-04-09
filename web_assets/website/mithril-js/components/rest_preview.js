import CarbonModal from 'carbon-components/src/components/modal/modal';
import m from 'mithril/hyperscript';
import m_redraw from 'mithril/redraw';
import createStore from 'unistore';
import { mapActions } from 'unistore/src/util';
//--
import { msgbus } from '../../../misc/msgbus';
import { Slot } from '../../../carbondesign/mithril-js/base';
import { Modal } from '../../../carbondesign/mithril-js/modal';

const StoreActions =
{
    setPreview(state, preview)
    {
        return {preview: preview}
    },
}


export class RestPreviewModal
{
    constructor(app, trigger_element)
    {
        this.app = app;
        this.trigger_element = trigger_element;
        this.txt_title = gettext("Preview");
    }

    oninit(vnode)
    {
        this.store = createStore({
            preview: '',
        });
        this.actions = mapActions(StoreActions, this.store);
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

    async oncreate(vnode)
    {
        this.component = CarbonModal.create(vnode.dom);

        let textarea = document.getElementById(
                this.trigger_element.getAttribute('data-provide-rest-preview'));

        this.component.show(this.trigger_element);

        let formData = new FormData();
        formData.append('body', textarea.value);
        let resp = await msgbus('/api/render-html').body(formData).post();
        let html = await resp.text();
        this.actions.setPreview(html);
        m_redraw();

        // Catch the modal being closed
        vnode.dom.addEventListener('modal-hidden', () => this.app.stopModal());
    }

    onremove(vnode)
    {
        this.component.release();
    }
}


export function inject_rest_preview(element, app)
{
    element.addEventListener('click', function()
    {
        app.startModal(new RestPreviewModal(app, element));
    });
}
