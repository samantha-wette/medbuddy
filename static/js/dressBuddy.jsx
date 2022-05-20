function Test() {
    const [userInfo, setUserInfo] = React.useState({});

    React.useEffect(() => {
        fetch('/data')
        .then((response) => response.json())
        .then((result) => {
            setUserInfo(result);
            console.log(result.accessories[0].name);
        });
    }, []);
    const accessoryItems = [];
    if (userInfo.length === 0) {
        return<p>Nothing yet</p>;
    }
    if ("accessories" in userInfo) {
        for (const accessory of userInfo.accessories) {
            accessoryItems.push(<li key={accessory.id}>{accessory.name}</li>);

        }
    }
    return<ul>Hi, {userInfo.fname}! Your accessories are:
    {accessoryItems}
    
    
    </ul>;
}

ReactDOM.render(<Test />, document.querySelector('#container'));