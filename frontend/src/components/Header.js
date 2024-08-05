import React from "react"

class Header extends React.Component {
    render() {
           return (
           <header className='header'>
                {this.props.my_text}
            </header>
           )
    }
}

export default Header