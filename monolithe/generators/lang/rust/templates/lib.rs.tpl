{{header}}

extern crate serde;
#[macro_use]
extern crate serde_derive;
extern crate serde_json;
extern crate bambou;
extern crate reqwest;

{% for spec in specifications %}
mod {{spec.entity_name.lower() }};
{%- endfor %}

{% for spec in specifications %}
pub use {{spec.entity_name.lower() }}::{{spec.entity_name}};
{%- endfor %}
