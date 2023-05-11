import Avatar from '@mui/material/Avatar';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { useHistory } from "react-router-dom";
import Rating, { ratingClasses } from '@mui/material/Rating';
import StarIcon from '@mui/icons-material/Star';

function Profile({ user, setUser }) {
    const history = useHistory();
    const handleDelete = () => {
        fetch(`/user/${user.id}`, {
          method: 'DELETE',
        })
          .then((res) => {
            if (res.ok) {
              return res.json();
            }
            throw new Error('Network broken');
          })
          .then(() => {
            window.alert('User deleted successfully!');
            setUser(undefined);
          })
          .catch((error) => {
            console.error(error);
          });
          history.push('/home');
      };
    function handleEdit() {
        history.push("/edit")
    }
    return (
        <Box>
        <Box sx= {{
            ml:"45%",
            mt:"15%",
            alignItems: 'center'
        }}>
        {user && user.id && user.avatar && user.username && (
        <Avatar
        sx={{
            width: "18%",
            height: "18%",
            alignItems: 'center'
        }}
            sizes="lg"
            src={user.avatar}
        />
        )}
        {user && user.username && (
        <Typography component="h1" variant="h5" sx={{
            ml:"7%",
            mt:3
        }}>
            {user.username}
          </Typography>
          )}
        {user && user.rating && (
        <Rating
        sx={{ml:"4.27%",
        mt:3}}
  name="text-feedback"
  value={user.rating}
  readOnly
  precision={0.5}
  emptyIcon={<StarIcon style={{ opacity: 0.55 }} fontSize="inherit" />}
/>
)}
        </Box>
        </Box>
    )
}

export default Profile