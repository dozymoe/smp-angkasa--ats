import CarbonModal from 'carbon-components/src/components/modal/modal';
import m from 'mithril/hyperscript';
import m_redraw from 'mithril/redraw';
import createStore from 'unistore';
import { mapActions } from 'unistore/src/util';
//--
import { msgbus } from '../../../misc/msgbus';
import { Slot } from '../../../carbondesign/mithril-js/base';
import { Modal } from '../../../carbondesign/mithril-js/modal';
import { Table, Th, Td, TdOvButton
       } from '../../../carbondesign/mithril-js/data-table';
import { Pagination } from '../../../carbondesign/mithril-js/pagination';
import { get_pager } from '../../../misc/pagination';

const ATTRIBUTE_NAME = 'data-provide-select_page';


const StoreActions =
{
    setObjects(state, objects)
    {
        return {objects: objects}
    },

    setPager(state, pager)
    {
        return {pager: pager}
    }
}


export class SelectPageModal
{
    constructor(app, trigger_element)
    {
        this.app = app;
        this.trigger_element = trigger_element;
        this.txt_title = gettext("Page Select");
    }

    oninit(vnode)
    {
        this.store = createStore({
            pager: get_pager({}),
            objects: [],
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
  m(Table, null,
    [
      m(Slot, {name: 'title'}, gettext("Pages")),
      m(Slot, {name: 'head'},
        [
          m(Th, null, gettext("Id")),
          m(Th, null, gettext("Title")),
          m(Th, null, gettext("Summary")),
          m(Th, {mode: 'menu'}),
        ]),

      ...state.objects.map(obj =>
        m('tr', null,
          [
            m(Td, null, obj.id),
            m(Td, null, obj.title),
            m(Td, null, obj.summary),
            m(Td, {mode: 'menu'},
              [
                m(TdOvButton,
                  {
                    onclick: () => this.onselect_click(obj),
                  },
                  gettext("Select")),
              ]),
          ])
        ),
      m(Slot, {name: 'pagination'},
        m(Pagination,
          {
            pager: state.pager,
            pager_size: state.pager.paginator.per_page,
          })),
    ]),
  ])
//##
        )
    }

    async oncreate(vnode)
    {
        this.component = CarbonModal.create(vnode.dom);

        let textarea = document.getElementById(
                this.trigger_element.getAttribute(ATTRIBUTE_NAME));

        this.component.show(this.trigger_element);

        let resp = await msgbus('/api/web_pages/').get();
        let body = await resp.json();
        this.actions.setPager(get_pager(body));
        this.actions.setObjects(body.results);
        m_redraw();

        // Catch the modal being closed
        vnode.dom.addEventListener('modal-hidden', () => this.app.stopModal());
    }

    onremove(vnode)
    {
        this.component.release();
    }

    onselect_click(obj)
    {
        let elValue = document.getElementById(
                this.trigger_element.getAttribute(ATTRIBUTE_NAME));
        let elLabel = document.getElementById(
                this.trigger_element.getAttribute('data-select_page-label'));
        elValue.value = obj.id;
        elLabel.value = obj.title;
        this.component.hide();
    }
}


export function inject_select_page(element, app)
{
    element.addEventListener('click', function()
    {
        app.startModal(new SelectPageModal(app, element));
    });
}
