function BuddyDiv(props) {
    return(<div className="card">
    <div className="card-body">
    <img className="card-img-top" src={props.img} alt={props.alt} />
        <h5 className="card-title">{props.name}</h5>
        <a href="#">Set as Primary Buddy</a>
    </div>
    </div>)
}

function SelectPrimaryBuddy(props) {
    const[name, setName] = React.useState('')
    const [buddy, setBuddy] = React.useState('')
    function selectBuddy() {
        fetch("/select-buddy", {
            methods: ["POST", "GET"],
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({"name": name, "buddy": buddy}),
        })
        .then((response) => response.json())
        .then((jsonResponse) => {
            const buddySelected = jsonResponse.buddySelected;
            props.selectBuddy(buddySelected);
        });
    }
    return(
        <React.Fragment>
            <h2>Pick your primary buddy!</h2>
            <label htmlFor="nameInput">
                Name Your Buddy:
                <input value={name}
                onChange={(event) => setName(event.target.value)}
                id="nameInput"
                />            
            </label>
            <label htmlFor="buddySelection">
                Choose Your Main Buddy:
                <input value={buddy}
                onChange={(event) => setBuddy(event.target.value)}
                id="buddySelection"
                />            
            </label>
            <button type="button" onClick={selectBuddy}>
        Pick Me!
      </button>
        </React.Fragment>
    )}


// const createDivsForBuddies = (buddies) => {
//             const buddyContainer = document.getElementById('#buddy-container');
//             for (const buddy of buddyItems) {
//                 console.log(buddy)
//                 console.log("*****")
//                 buddyContainer.insertAdjacentHTML('beforeend', `<div class="buddy-box $">${buddy.name}</div>`);

//             }
//         }

function DressUp() {
    const [userInfo, setUserInfo] = React.useState({});

    React.useEffect(() => {
        fetch('/data')
        .then((response) => response.json())
        .then((result) => {
            setUserInfo(result);
        });
    }, []);
    
    if (userInfo.length === 0) {
        return<p>Nothing yet</p>;
    }
    const buddyItems = [];

    if ("buddies" in userInfo) {
        for (const buddy of userInfo.buddies) {
            buddyItems.push(
                <BuddyDiv
                key={buddy.name}
                name={buddy.name}
                img={buddy.img1}
                alt={buddy.alt1}
                />
            );
        }
        }
    return(
    <React.Fragment>
        <SelectPrimaryBuddy selectBuddy={selectBuddy} />
      <h2>Buddies</h2>
      <div className="grid">{buddyItems}</div>
    </React.Fragment>
    )
    // const accessoryItems = [];

    // if ("accessories" in userInfo) {
    //     for (const accessory of userInfo.accessories) {
    //         accessoryItems.push(<li key={accessory.id}>{accessory.name}</li>);
    //     }



    // return<ul>Hi, {userInfo.fname}! You've got buddies!
    

    // </ul>;
}

ReactDOM.render(<DressUp />, document.querySelector('#buddy-container'))
