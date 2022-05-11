function SideBarItem({text, Icon} : {text: string, Icon: any}) {
    return (
        <div className = 'link'>
            <Icon />
            <h2>{text}</h2>
        </div>
    );
}

export default SideBarItem;