import React from 'react'
import axios from 'axios'
import baseurl from './RoutesLinks'
import SimpleDateTime  from 'react-simple-timestamp-to-date';

//import { useTable } from 'react-table'
import { format } from 'date-fns'



class ListDrivers extends React.Component {
    constructor(props)
            {
              super(props)

              const dateString = format(this.props.my_date, 'yyyy-MM-dd')

              const timestamp = Date.parse(this.props.my_date)
              const date_1 = new Intl.DateTimeFormat('en-EN', {year: 'numeric', month: '2-digit',day: '2-digit'}).format(this.props.my_date)


              const da = '2024-02-02'

               axios.get(baseurl+'/driver/'+dateString+'/').then((res) => {
                      this.setState({driver_date: res.data.car_carrier })
               })


               this.state = {
                             driver_date: [],
                             date: format(this.props.my_date, 'yyyy-MM-dd')
                             }
            }
    render() {
    console.log(baseurl+'/driver/'+this.state.date+'/')
           if (this.state.driver_date.length > 0)
            return (
                <div>
                    {this.state.driver_date.map((driver) => (
                        <div className="block_driver" key={driver.id_driver}>
                            <h3>{driver.people.first_name} {driver.people.last_name}</h3>
                            <p>{driver.people.driving_licence}</p>
                        </div>
                    ))}
                </div>
            )
        else
            return (
                <div className="block_user">
                    <h3>Нет водителей</h3>
                </div>
            )
    }
}

export default ListDrivers