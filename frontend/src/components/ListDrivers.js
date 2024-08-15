import React from 'react'
//import { useTable } from 'react-table'

class ListDrivers extends React.Component {
    render() {
           if (this.props.driver_date.length > 0)
            return (
                <div>
                    {this.props.driver_date.map((driver) => (
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