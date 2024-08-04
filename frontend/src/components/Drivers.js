import React from "react"
//import User from "./User"

class Drivers extends React.Component {
    render() {
        if (this.props.drivers.length > 0)
            return (
                <div>
                    {this.props.drivers.map((driver) => (
                        <div className="block_driver" key={driver.id_driver}>
                            <h3>{driver.people.first_name} {driver.people.last_name}</h3>
                            <p>{driver.date_trip}</p>
                        </div>
                    ))}
                </div>
            )
        else
            return (
                <div className="block_user">
                    <h3>Пользователей нет</h3>
                </div>
            )
    }
}

export default Drivers