import { inject } from 'mobx-react';
import React, { Component } from 'react';
//-
import { msgbus } from '../../../../../misc/msgbus.js';
import { Dialog
       } from '../../../../../../lib/react-materialweb/js/views/dialog.jsx';


@inject('app')
export class ReSTPreview extends Component
{
    constructor(props)
    {
        super(props);
        this.state = {html: ''};
    }

    async componentDidMount()
    {
        let formData = new FormData();
        formData.append('body', this.props.markup);
        let response = await msgbus('/api/render-html').body(formData).post();
        let html = await response.text();
        this.setState({html: html});
    }

    render()
    {
        let elPage = document.getElementById('page-wrapper');

        return (

<Dialog visible={this.props.show} onClose={this.props.onHide}
    outsideElement={elPage}>

  <Dialog.Title>
    {this.props.title}
  </Dialog.Title>

  <Dialog.Content>
    <div dangerouslySetInnerHTML={{__html: this.state.html}}></div>
  </Dialog.Content>

  <Dialog.Actions>
    <Dialog.Button action={Dialog.Actions.SUBMIT}>
      Close
    </Dialog.Button>
  </Dialog.Actions>
</Dialog>

        );
    }
}
