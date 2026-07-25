const AuthCard = ({children}) => {
    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">

    <div className="w-full max-w-md rounded-xl bg-white shadow-lg p-8">

        {children}

    </div>

</div>
    );
};

export default AuthCard;