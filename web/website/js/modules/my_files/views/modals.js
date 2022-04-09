//-
import { msgbus } from '../../../../../misc/msgbus';
import { DataTable
       } from '../../../../../../lib/react-materialweb/js/views/data-table.jsx';
import { Dialog
       } from '../../../../../../lib/react-materialweb/js/views/dialog.jsx';
import { get_pager } from '../../../misc/pagination';


@inject('app')
export class SelectFile extends Component
{
    constructor(props)
    {
        super(props);
        this.state = {pager: {results: []}};
    }

    select(record)
    {
        this.props.resolve(record);
        this.props.onHide();
    }

    async componentDidMount()
    {
        let res = await msgbus('/api/files/?test=hallo', {}).get();
        let pager = await res.json();
        if (pager)
        {
            this.setState({pager: pager});
        }
    }

    render()
    {
        let pager = get_pager(this.state.pager);
        console.log(pager);

        return (

<Dialog visible={this.props.show} onClose={this.props.onHide}>
  <Dialog.Title>{this.props.title}</Dialog.Title>

  <Dialog.Content>
    <DataTable pager={pager}>
      <DataTable.Head>
        <DataTable.Head.Row>
          <DataTable.Head.Col>
            ID
          </DataTable.Head.Col>
          <DataTable.Head.Col>
            Image
          </DataTable.Head.Col>
          <DataTable.Head.Col>
            Description
          </DataTable.Head.Col>
          <DataTable.Head.Col>
            Actions
          </DataTable.Head.Col>
        </DataTable.Head.Row>
      </DataTable.Head>
      <DataTable.Body>
      {this.state.pager.results.map(record =>
          <DataTable.Row key={record.id}>
            <DataTable.ColHeader>
              {record.id}
            </DataTable.ColHeader>
            <DataTable.Col>
              <img height="100" src={record.attr_src}
                  srcset={record.attr_srcset} sizes={record.attr_sizes}
                  style={{margin: 4}} />
            </DataTable.Col>
            <DataTable.Col>{record.description}</DataTable.Col>
            <DataTable.Col>
              <button onClick={() => this.select(record)}>Select</button>
            </DataTable.Col>
          </DataTable.Row>
          )}
      </DataTable.Body>
    </DataTable>
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

/*
{
    "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 2,
                "description": "Picture",
                "alt_text": "foto",
                "databits": "/uploads/files/original/e6649eea-4408-4f2b-a237-a8ebb16ea1a2.jpeg",
                "image_xs": "/uploads/files/image_xs/e6649eea-4408-4f2b-a237-a8ebb16ea1a2.jpeg",
                "image_sm": "/uploads/files/image_sm/e6649eea-4408-4f2b-a237-a8ebb16ea1a2.jpeg",
                "image_md": "/uploads/files/image_md/e6649eea-4408-4f2b-a237-a8ebb16ea1a2.jpeg",
                "image_lg": "/uploads/files/image_lg/e6649eea-4408-4f2b-a237-a8ebb16ea1a2.jpeg",
                "created_at": "2022-02-06T09:55:37.121076+07:00"
            },
            {
                "id": 1,
                "description": "Elevation",
                "alt_text": "large elevation",
                "databits": "/uploads/files/original/800px-LARGE_elevation_1D86uwS.jpg",
                "image_xs": "/uploads/files/image_xs/800px-LARGE_elevation_1D86uwS.jpg",
                "image_sm": "/uploads/files/image_sm/800px-LARGE_elevation_1D86uwS.jpg",
                "image_md": "/uploads/files/image_md/800px-LARGE_elevation_1D86uwS.jpg",
                "image_lg": null,
                "created_at": "2022-02-06T09:54:51.881511+07:00"
            }
        ]
}
*/
