function MedCard(props) {
    return(<div className="card">
    <div className="card-body">
        <h5 className="card-title">{props.name}</h5>
        <a href={props.info} className="btn btn-primary">Learn More</a>
    </div>
    </div>)
}


function MedCardContainer() {
    const [userInfo, setUserInfo] = React.useState({});

    React.useEffect(() => {
        fetch('/data')
        .then((response) => response.json())
        .then((result) => {
            setUserInfo(result);
        });
    }, []);
    const userMeds = []; 
    if (userInfo.length === 0) {
        return<p>Nothing yet</p>;
    }
    if ("meds" in userInfo) {
        for (const currentMed of userInfo.meds) {
            userMeds.push(
            <MedCard
            key={currentMed.id}
            name={currentMed.name}
            info={currentMed.information}
            official={currentMed.official}
            
            />
            );
        }
    }
    return<div>
    {userMeds}
    </div>;
}
  
ReactDOM.render(<MedCardContainer />, document.querySelector('#container'));
