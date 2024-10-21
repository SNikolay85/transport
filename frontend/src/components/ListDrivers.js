import React from 'react'
import axios from 'axios'
import baseurl from './AppRoute'

//import { useTable } from 'react-table'

class ListDrivers extends React.Component {
    constructor(props)
            {
              super(props)

               axios.get(baseurl + '/driver/2024-02-01/').then((res) => {
                      this.setState({driver_date: res.data.car_carrier })
               })


               this.state = {
                             date_now: new Date(),
                             driver_date: [],
                             }
            }
    render() {
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