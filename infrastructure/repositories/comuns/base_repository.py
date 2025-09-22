class BaseRepository:
    def __init__(self, session, model, mapper):
        self.session = session
        self.model = model
        self.mapper = mapper

    def add(self, entity):
        model_instance = self.mapper.to_model(entity)
        self.session.add(model_instance)
        self.session.commit()
        return self.mapper.to_entity(model_instance)

    def get_all(self):
        results = self.session.query(self.model).all()
        return [self.mapper.to_entity(item) for item in results]

    def get_by_id(self, id_entity):
        model_instance = self.session.query(self.model).filter_by(id=id_entity).first()
        return self.mapper.to_entity(model_instance) if model_instance else None

    def delete(self, entity):
        model_instance = self.mapper.to_model(entity)
        self.session.delete(model_instance)
        self.session.commit()