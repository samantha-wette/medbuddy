CREATE TABLE "public.users" (
	"user_id" serial NOT NULL,
	"email" VARCHAR(255) NOT NULL,
	"password" serial(255) NOT NULL,
	"fname" VARCHAR(255) NOT NULL,
	"lname" VARCHAR(255),
	"points" integer,
	CONSTRAINT "users_pk" PRIMARY KEY ("user_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.accessories" (
	"item_id" serial NOT NULL,
	"item_name" VARCHAR(255) NOT NULL,
	"item_cost" integer NOT NULL,
	"item_description" TEXT,
	"item_img" VARCHAR(255) NOT NULL,
	CONSTRAINT "accessories_pk" PRIMARY KEY ("item_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.medications" (
	"medication_id" serial NOT NULL,
	"generic_name" VARCHAR(255) NOT NULL,
	"brand_name" VARCHAR(255),
	"med_information" VARCHAR(255),
	CONSTRAINT "medications_pk" PRIMARY KEY ("medication_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.buddies" (
	"buddy_id" serial NOT NULL,
	"buddy_name" VARCHAR(255) NOT NULL,
	"buddy_description" TEXT,
	"buddy_img" VARCHAR(255) NOT NULL,
	"user_id" integer NOT NULL,
	CONSTRAINT "buddies_pk" PRIMARY KEY ("buddy_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.user_meds" (
	"user_id" integer NOT NULL,
	"medication_id" integer NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.user_inventory" (
	"user_id" integer NOT NULL,
	"item_id" integer NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.wearable_by" (
	"item_id" BINARY NOT NULL,
	"buddy_id" BINARY NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.med_schedule" (
	"date_time" DATETIME NOT NULL,
	"user_id" integer NOT NULL,
	"medication_id" integer NOT NULL,
	"taken" BOOLEAN NOT NULL
) WITH (
  OIDS=FALSE
);






ALTER TABLE "buddies" ADD CONSTRAINT "buddies_fk0" FOREIGN KEY ("user_id") REFERENCES "users"("user_id");

ALTER TABLE "user_meds" ADD CONSTRAINT "user_meds_fk0" FOREIGN KEY ("user_id") REFERENCES "users"("user_id");
ALTER TABLE "user_meds" ADD CONSTRAINT "user_meds_fk1" FOREIGN KEY ("medication_id") REFERENCES "medications"("medication_id");

ALTER TABLE "user_inventory" ADD CONSTRAINT "user_inventory_fk0" FOREIGN KEY ("user_id") REFERENCES "users"("user_id");
ALTER TABLE "user_inventory" ADD CONSTRAINT "user_inventory_fk1" FOREIGN KEY ("item_id") REFERENCES "accessories"("item_id");

ALTER TABLE "wearable_by" ADD CONSTRAINT "wearable_by_fk0" FOREIGN KEY ("item_id") REFERENCES "accessories"("item_id");
ALTER TABLE "wearable_by" ADD CONSTRAINT "wearable_by_fk1" FOREIGN KEY ("buddy_id") REFERENCES "buddies"("buddy_id");

ALTER TABLE "med_schedule" ADD CONSTRAINT "med_schedule_fk0" FOREIGN KEY ("user_id") REFERENCES "users"("user_id");
ALTER TABLE "med_schedule" ADD CONSTRAINT "med_schedule_fk1" FOREIGN KEY ("medication_id") REFERENCES "medications"("medication_id");









