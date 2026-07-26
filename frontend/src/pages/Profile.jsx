import { useEffect, useState } from "react";
import { getCurrentUser } from "../api/authApi";

function Profile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const data = await getCurrentUser();
        setUser(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center py-10">
        Loading...
      </div>
    );
  }

  if (!user) {
    return (
      <div className="rounded-xl bg-white p-8 shadow">
        Failed to load profile.
      </div>
    );
  }

  return (
    <div className="max-w-3xl rounded-xl bg-white p-8 shadow-sm border">
      <h1 className="text-3xl font-bold mb-8">
        My Profile
      </h1>

      <div className="grid md:grid-cols-2 gap-6">

        <div>
          <p className="text-sm text-gray-500">
            Full Name
          </p>

          <p className="font-semibold text-lg">
            {user.full_name}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-500">
            Email
          </p>

          <p className="font-semibold">
            {user.email}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-500">
            Account Status
          </p>

          <span
            className={`inline-block rounded-full px-3 py-1 text-sm ${
              user.is_active
                ? "bg-green-100 text-green-700"
                : "bg-red-100 text-red-700"
            }`}
          >
            {user.is_active ? "Active" : "Inactive"}
          </span>
        </div>

        <div>
          <p className="text-sm text-gray-500">
            Email Verification
          </p>

          <span
            className={`inline-block rounded-full px-3 py-1 text-sm ${
              user.is_verified
                ? "bg-green-100 text-green-700"
                : "bg-yellow-100 text-yellow-700"
            }`}
          >
            {user.is_verified ? "Verified" : "Not Verified"}
          </span>
        </div>

        <div>
          <p className="text-sm text-gray-500">
            Joined
          </p>

          <p>
            {new Date(user.created_at).toLocaleDateString()}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-500">
            Last Updated
          </p>

          <p>
            {new Date(user.updated_at).toLocaleDateString()}
          </p>
        </div>

      </div>
    </div>
  );
}

export default Profile;