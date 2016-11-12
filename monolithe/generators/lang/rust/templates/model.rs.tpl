{{ header }}

use bambou::{Error, RestEntity, Session};
use reqwest::Response;
use std::collections::BTreeMap;
use serde_json;

{% for api in specification.child_apis %}{%- if api.rest_name != specification.rest_name -%}{% set child_spec = specification_set[api.rest_name] %}
pub use {{child_spec.entity_name.lower() }}::{{child_spec.entity_name}};{%- endif -%}
{%- endfor %}


#[derive(Serialize, Deserialize, Default, Debug)]
pub struct {{specification.entity_name}}<'a> {
    #[serde(skip_serializing)]
    #[serde(skip_deserializing)]
    _session: Option<&'a Session>,

    #[serde(rename="ID")]
    id: Option<String>,{% if specification.is_root %}

    #[serde(rename = "APIKey")]
    api_key: Option<String>,{% else %}

    #[serde(rename="parentID")]
    parent_id: Option<String>,

    #[serde(rename="parentType")]
    parent_type: Option<String>,

    owner: Option<String>,{% endif %}

    {% for attribute in specification.attributes %}{% if attribute.local_name != attribute.name %}
    #[serde(rename="{{attribute.name}}")]{% endif %}
    pub {{attribute.local_name}}: {{attribute.local_type}},
    {% endfor %}
}

impl<'a> RestEntity<'a> for {{specification.entity_name}}<'a> {
    fn fetch(&mut self) -> Result<Response, Error> {
        match self._session {
            Some(session) => session.fetch_entity(self),
            None => Err(Error::NoSession),
        }
    }

    fn save(&mut self) -> Result<Response, Error> {
        match self._session {
            Some(session) => session.save(self),
            None => Err(Error::NoSession),
        }
    }

    fn delete(self) -> Result<Response, Error> {
        match self._session {
            Some(session) => session.delete(self),
            None => Err(Error::NoSession),
        }
    }

    fn create_child<C>(&self, child: &mut C) -> Result<Response, Error>
        where C: RestEntity<'a>
    {
        match self._session {
            Some(session) => session.create_child(self, child),
            None => Err(Error::NoSession),
        }
    }

    fn path() -> &'static str {
        "{{specification.rest_name}}"
    }

    fn group_path() -> &'static str {
        "{{specification.resource_name}}"
    }

    fn is_root(&self) -> bool {
        {% if specification.is_root %}true{% else %}false{% endif %}
    }

    fn id(&self) -> Option<&str> {
        self.id.as_ref().and_then(|id| Some(id.as_str()))
    }

    fn fetch_children<R>(&self, children: &mut Vec<R>) -> Result<Response, Error>
        where R: RestEntity<'a>
    {
        match self._session {
            Some(session) => session.fetch_children(self, children),
            None => Err(Error::NoSession),
        }
    }

    fn get_session(&self) -> Option<&Session> {
        self._session
    }

    fn set_session(&mut self, session: &'a Session) {
        self._session = Some(session);
    }
}

impl<'a> {{specification.entity_name}}<'a> {
{% for api in specification.child_apis %}{% set child_spec = specification_set[api.rest_name] %}
    pub fn fetch_{{ child_spec.resource_name }}(&self) -> Result<Vec<{{child_spec.entity_name}}>, Error> {
        let mut {{ child_spec.resource_name }} = Vec::<{{child_spec.entity_name}}>::new();
        let _ = self.fetch_children(&mut {{child_spec.resource_name}})?;
        Ok({{ child_spec.resource_name }})
    }
{% endfor -%}
}
