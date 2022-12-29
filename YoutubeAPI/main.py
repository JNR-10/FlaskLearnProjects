from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app) # wrapping our app in an API
app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"

# creating a model to store videos
db.create_all()

""" making a new RequestParser object. This will automatically parse through the object we are 
sending and fits the guidelines that we are going to define"""
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
# help means what shoud be sent ot user if they don't send the information
# like an error message
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)
# now the information is compulsory requirement

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")

resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'views': fields.Integer,
	'likes': fields.Integer
}
videos = {}

def abort_if_video_id_doesnt_exists(video_id):
    if video_id not in videos:
        abort(404, message="Could not find video...")
"""
def abort_if_video_exists(video_id):
    if video_id in videos:
        abort(409, message="Video already exists")

class Video(Resource):
    def get(self, video_id):
        abort_if_video_id_doesnt_exists(video_id)
        return videos[video_id]

    #create a new videos (dictionary)
    def put(self, video_id):
        abort_if_video_exists(video_id) # so that we do not create a video that already exists
        #get all the arguments
        args = video_put_args.parse_args()
        # adding videos and associating with the data
        videos[video_id] = args
        return videos[video_id], 201 #created

    def delete(self, video_id):
        abort_if_video_id_doesnt_exists(video_id)
        del videos[video_id]
        return '', 204 #deleted successfully

api.add_resource(Video, "/video/<int:video_id>") """

class Video(Resource):
    #decorator
	@marshal_with(resource_fields) # take the returned result and serialise with specified resourse field
	def get(self, video_id):
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="Could not find video with that id")
		return result

	@marshal_with(resource_fields)
	def put(self, video_id):
		args = video_put_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		if result:
			abort(409, message="Video id taken...")

		video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
		db.session.add(video)
		db.session.commit()
		return video, 201

	@marshal_with(resource_fields)
	def patch(self, video_id):
		args = video_update_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="Video doesn't exist, cannot update")

		if args['name']:
			result.name = args['name']
		if args['views']:
			result.views = args['views']
		if args['likes']:
			result.likes = args['likes']

		db.session.commit()

		return result


	def delete(self, video_id):
		abort_if_video_id_doesnt_exists(video_id)
		del videos[video_id]
		return '', 204

if __name__ == "__main__":
    app.run(debug = True)